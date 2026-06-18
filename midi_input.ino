#include <SPI.h>
#include <MIDI.h>

// SoftwareSerial på pind 8 (RX) og pind 9 (TX)
MIDI_CREATE_DEFAULT_INSTANCE();

// =====================================================
// CONFIG
// =====================================================

#define QUEUE_SIZE 64

// =====================================================
// MIDI EVENT STRUCT
// =====================================================



// =====================================================
// QUEUE & DATA STATS (volatile pga. ISR brug)
// =====================================================

volatile byte schlange[QUEUE_SIZE];

 int queueHead = 0;
 int queueTail = 0;
 byte Nullvalue = 0; 

// Nuværende event der sendes over SPI
volatile byte currentEvent = Nullvalue ;



bool queueIsEmpty()
{
    return queueHead == queueTail;
}

bool queueIsFull()
{
    return ((queueHead + 1) % QUEUE_SIZE) == queueTail;
}

// Push event kaldes fra den almindelige main loop (MIDI callbacks)
void pushEvent(int event)
{
    if (queueIsFull())
    {
        // Køen er fuld - event droppes for at beskytte RAM
        return;
    }

    schlange[queueHead] = event;


    queueHead = (queueHead + 1) % QUEUE_SIZE;
}

// =====================================================
// MIDI CALLBACK FUNKTIONER
// =====================================================

void handleNoteOn(byte channel, byte pitch, byte velocity)
{
    pushEvent(pitch);
}

void handleNoteOff(byte channel, byte pitch, byte velocity)
{
    pitch = pitch + 128;
    pushEvent(pitch);
}



// System Real-Time: Start (0xFA)
void handleStart()
{
    pushEvent(1);
}

// System Real-Time: Timing Clock (0xF8)
void handleClock()
{
    pushEvent(3);
}

// System Real-Time: Stop (0xFC)
void handleStop()
{
    pushEvent(2);
}

// =====================================================
// SPI INTERRUPT (Udløses automatisk når master overfører en byte)
// =====================================================

ISR(SPI_STC_vect)
{
    // Vi læser det modtagne data for at tømme bufferen (selvom vi primært sender)
    //byte receivedByte = SPDR;

  
        if (queueIsEmpty())
        {
            // Hvis køen er tom, sender vi nul-events (Idling)
            currentEvent = Nullvalue;
        }
        else
        {
            // Hent næste event direkte i ISR for trådsikkerhed
            currentEvent = schlange[queueTail];
            queueTail = (queueTail + 1) % QUEUE_SIZE;
        }
    
          SPDR = currentEvent; // Næste clock 
  
}

// =====================================================
// SETUP
// =====================================================

void setup()
{
    pinMode(SS,INPUT_PULLUP);
    pinMode(MOSI,INPUT_PULLUP);
    pinMode(SCK,INPUT);
    pinMode(MISO,OUTPUT);
    SPCR |= _BV(SPE) | _BV(SPIE);
    SPDR = currentEvent;
    SPI.attachInterrupt();
    MIDI.setHandleNoteOn(handleNoteOn);
    MIDI.setHandleNoteOff(handleNoteOff);
    MIDI.setHandleStart(handleStart);
    MIDI.setHandleClock(handleClock);
    MIDI.setHandleStop(handleStop);
    MIDI.begin(16);
    MIDI.turnThruOn();
}

// =====================================================
// LOOP
// =====================================================

void loop()
{
    MIDI.read();
}



