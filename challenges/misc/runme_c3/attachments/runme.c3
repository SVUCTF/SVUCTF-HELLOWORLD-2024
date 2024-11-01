module runme;
import std::io;

const uint[] ENCRYPTED_FLAG = {
    0xb5d505a5, 0x36f0f774, 0x8036f4d0, 0xc0f4f0b4, 0x14d1f015
};

const uint MAGIC = 0xC3;

fn void decrypt(uint[] data)
{
    foreach (&value : data)
    {
        for (int i = 0; i < 4; i++)
        {
            uint byte = (*value >> (8 * i)) & 0xFF;
            byte ^= MAGIC & 0xFF;
            byte = ((byte >> 4) | (byte << 4)) & 0xFF;
            *value &= ~(0xFF << (8 * i));
            *value |= byte << (8 * i);
        }
    }
}

fn void print_flag(uint[] data)
{
    foreach (value : data)
    {
        for (int i = 0; i < 4; i++)
        {
            char c = (char)(value & 0xFF);
            io::printf("%c", c);
            value >>= 8;
        }
    }
    io::printn();
}

fn void main()
{
    uint[] flag = ENCRYPTED_FLAG;
    decrypt(flag);
    print_flag(flag);
}

