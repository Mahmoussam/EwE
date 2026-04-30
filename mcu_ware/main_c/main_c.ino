
#include <SPI.h>

#include "E_Serial/src/E_Serial.h"

#define READ 0
#define WRITE 1

#define DEBUG_LED 8
// Chip select pin
#define SS 10

#define MSG_SIZE MSG_LEN
#define START_BYTE '!'

byte rxBuffer[MSG_SIZE];
byte rxIndex = 0;
bool msgReady = false;

bool state13 = false;
volatile uint8_t g_daisy_chain_length = 1;

void send_serial_sig(){
	char sig[]  = {'!' , 1 , 2 , 3 , 4 , 5 , 8};
	sendMessage(sig);
}

static uint8_t Calculate_SPI_CRC(uint16_t wData) {
  uint8_t crc = 0x42;
  uint8_t data[2] = {(uint8_t)((wData >> 8) & 0xFF), (uint8_t)(wData & 0xFF)};

  for (uint8_t i = 0; i < 2; ++i) {
    crc ^= data[i];
    for (uint8_t bit = 0; bit < 8; ++bit) {
      uint8_t msb = (uint8_t)(crc & 0x80);
      crc <<= 1;
      if (msb) crc ^= 0x2F;
    }
  }

  return crc;
}

void setup()
{
	// Serial comm to PC init
	Serial.begin(9600);
	while (!Serial)
	{
		delay(10);
	}
	// SPI to GD init

	pinMode(SS, OUTPUT);
	digitalWrite(SS, HIGH);

	SPI.begin();

	pinMode(DEBUG_LED, OUTPUT);
	digitalWrite(DEBUG_LED , LOW);
	//send_serial_sig();
	
}

// ------------------------------------------------------
// Function: sendMessage
// Sends a full protocol message
// ------------------------------------------------------
void sendMessage(const byte *msg)
{
	Serial.write(msg, MSG_SIZE);
}
/** 
 * Function name: uint32_t SPI_shift_24bit
 * @brief Shifts 3 bytes frame and its CRC into SPI daisy chain .
 * 
 * @param uint32_t frame - 16 bit frame to shift in.
 * 
 * @return uint32_t - received 3 bytes from SPI channel.
 * 
 */
static uint32_t SPI_shift_24bit(uint32_t frame)
{
	uint32_t tx_frame = (frame << 8) | Calculate_SPI_CRC(frame);
	uint32_t rx = 0;

	rx |= ((uint32_t)SPI.transfer((tx_frame >> 16) & 0xFF)) << 16;
	rx |= ((uint32_t)SPI.transfer((tx_frame >> 8) & 0xFF)) << 8;
	rx |= ((uint32_t)SPI.transfer(tx_frame & 0xFF));

	return rx;
}

uint32_t DC_send(uint8_t rw, uint8_t addr, uint16_t data, uint8_t dx)
{
	if (g_daisy_chain_length == 0 || dx >= g_daisy_chain_length)
	{
		return 0;
	}

	uint32_t frame = 0;
	frame |= ((uint32_t)(rw & 0x01)) << 15;
	frame |= ((uint32_t)(addr & 0x1F)) << 10;
	frame |= ((uint32_t)(data & 0x03FF));

	uint32_t rx = 0;

	digitalWrite(SS, LOW);
	SPI.beginTransaction(SPISettings(
		4000000, // 4 MHz
		MSBFIRST,
		SPI_MODE0));
	// DX is zero based where first (index zero) chip is the one at MOSI
	(void)SPI_shift_24bit(frame);

	for (uint8_t i = 0; i < dx; ++i)
	{
		rx = SPI_shift_24bit(0);
	}

	SPI.endTransaction();
	digitalWrite(SS, HIGH);

	return rx;
}

uint32_t DC_read(uint8_t dx)
{
	if (g_daisy_chain_length == 0 || dx >= g_daisy_chain_length)
	{
		return 0;
	}

	uint32_t rx = 0;

	digitalWrite(SS, LOW);
	SPI.beginTransaction(SPISettings(
		4000000, // 4 MHz
		MSBFIRST,
		SPI_MODE0));

	// Align the chain so the desired chip's outgoing 24-bit frame reaches MOSI.
	for (uint8_t i = 0; i < (uint8_t)(g_daisy_chain_length - 1 - dx); ++i)
	{
		(void)SPI_shift_24bit(0);
	}

	rx = SPI_shift_24bit(0);

	SPI.endTransaction();
	digitalWrite(SS, HIGH);

	return rx;
}
void toggleDBG(){
	state13 = !state13;
	digitalWrite(DEBUG_LED, state13);
}
// ------------------------------------------------------
// Function: onMessageReceived
// Called when a full valid message is received
// ------------------------------------------------------
void onMessageReceived(const byte *raw_msg)
{
	
	//sendMessage(raw_msg);
	//return;
	SerialMessage msg;
	if (init_SerialMessage_from_bytes(raw_msg, &msg) == 0)
	{
		// echo
		/*char dmp[7] = {'!' , msg.addr , msg.addr , (msg.data >> 8) & 0xFF , msg.data & 0xFF , msg.dx , 101};
		sendMessage(dmp);*/

		
		SerialMessage response;
		uint8_t out[MSG_SIZE];
		if (msg.type == WR)
		{
			(void)DC_send(WRITE, msg.addr, msg.data, msg.dx);
			make_ACKSerialMessage(msg.addr, msg.data, msg.dx, msg.mid, &response);
			get_bytes_from_SerialMessage(out, &response);
		}
		else if (msg.type == RE)
		{
			//sendMessage(raw_msg);
			if(READ == 0 && msg.dx == 1)toggleDBG();	
			(void)DC_send(READ, msg.addr, 0, msg.dx);
			delay(10);
			uint32_t raw_frame = DC_read(msg.dx);
			uint16_t reg_value = (uint16_t)((raw_frame >> 8) & ((uint32_t) 0x03FF));
			

			make_ACKSerialMessage(msg.addr, reg_value, msg.dx, msg.mid, &response);
		}
		else if (msg.type == ACK)
		{
			// Host handshake extension: ACK with addr=0x01 carries daisy-chain length in dx.
			
			if (msg.addr == 0x01)
			{
				g_daisy_chain_length = max(msg.dx, 1);
				//make_ACKSerialMessage(4, 0xABCD, g_daisy_chain_length, 100, &response);
				make_ACKSerialMessage(5, msg.data, g_daisy_chain_length, msg.mid, &response);
			}
			// Host query extension: ACK with addr=0x02 asks MCU for current daisy-chain length.
			else if (msg.addr == 0x02)
			{
				make_ACKSerialMessage(msg.addr, msg.data, g_daisy_chain_length, msg.mid, &response);
			}
			else
			{
				// Reply with ACK so host can verify command receipt if needed.
				make_ACKSerialMessage(msg.addr, msg.data, msg.dx, msg.mid, &response);
			}

			
		}
		get_bytes_from_SerialMessage(out, &response);
		sendMessage(out);
	}
}

// ------------------------------------------------------
// Function: serialEvent
// Called automatically by Arduino core between loop() calls
// ------------------------------------------------------
void serialEvent()
{
	while (Serial.available() > 0)
	{
		byte b = Serial.read();
		// Serial.print(b);
		//  If we’re at start and see START_BYTE, begin buffering
		if (rxIndex == 0 && b != START_BYTE)
			continue; // ignore until we see '!'

		rxBuffer[rxIndex++] = b;

		if (rxIndex >= MSG_SIZE)
		{
			rxIndex = 0;
			msgReady = true;
			onMessageReceived(rxBuffer);
		}
	}
}

// ------------------------------------------------------
// Main loop
// ------------------------------------------------------
void loop()
{
	// Example: periodically send a message
	static unsigned long lastSend = 0;
	/*
	if (millis() - lastSend > 10000) {
	  lastSend = millis();

	  byte msg[MSG_SIZE] = {START_BYTE, 'H', 'E', 'L', 'L', 'O'};
	  sendMessage(msg);
	}*/
	serialEvent();
	// (serialEvent() runs automatically between loop iterations)
}

uint32_t gd3160_spi_transfer(uint8_t rw,
							 uint8_t addr,
							 uint16_t data)
{
	uint32_t frame = 0;

	frame |= ((uint32_t)(rw & 0x01)) << 23;
	frame |= ((uint32_t)(addr & 0x1F)) << 18;
	frame |= ((uint32_t)(data & 0x03FF)) << 8;

	uint8_t crc = Calculate_SPI_CRC((uint16_t)(frame >> 8));
	frame |= crc;

	uint32_t rx = 0;

	digitalWrite(SS, LOW);

	rx |= ((uint32_t)SPI.transfer((frame >> 16) & 0xFF)) << 16;
	rx |= ((uint32_t)SPI.transfer((frame >> 8) & 0xFF)) << 8;
	rx |= ((uint32_t)SPI.transfer(frame & 0xFF));

	digitalWrite(SS, HIGH);

	return rx;
}
