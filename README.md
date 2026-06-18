
# Welcome

I'm currently working on a new iteration of one of my very first inventions, better known as Sven Åge – also known as the monophonic sequencer with polyphonic playback.

Check out the video here:
https://www.youtube.com/watch?v=PgP3zGQpj28

This time, the project is built around an Arduino that receives MIDI data and forwards it to a Raspberry Pi 3B.

The reason I'm using an Arduino for MIDI handling is that I don't want the Raspberry Pi wasting CPU cycles or RAM on interpreting MIDI messages. On top of that, the Arduino gives me an extra TX pin, making it incredibly easy to implement MIDI Thru with just a single line of code.

This means that the Raspberry Pi only has to focus on one thing: MIDI Out.

Inside the Arduino firmware, the MIDI information is simplified. For example, a Note On message is represented as a single integer between 25 and 109. The reason for this limitation is that I'm using an Arturia Keystep as the reference keyboard, and its key range fits perfectly within those values. This leaves the range from 0 to 24 available for other MIDI functions such as Start, Stop, and Clock.

And you're probably thinking:

"What about velocity?"

To that, I only have one answer:

Fuck velocity.

If I want the sequencer to output different velocity values, that's something that should happen on the Raspberry Pi. There, I can fine-tune everything through a proper user interface consisting of rotary encoders and a 5-inch display.

After all, no human can consistently hit exactly the same velocity on a keyboard every single time.

The reason I'm rebuilding the machine is that I felt the original hardware was too limited. I want complete control over my sequencer and much more detailed note-by-note sequencing capabilities.

The sequencing workflow will take inspiration from modern sequencers such as the Arturia Keystep Pro, while the visual representation of entered notes will be closer to a classic tracker interface. This makes it possible to view many steps at once and get a much better overview of the sequence.

The goal is to combine the hands-on workflow of modern hardware sequencers with the clarity and precision of old-school tracker software.
