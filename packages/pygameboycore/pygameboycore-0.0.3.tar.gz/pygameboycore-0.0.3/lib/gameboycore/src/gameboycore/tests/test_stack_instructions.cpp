/**
	Test Stack Instructions on CPU

	@author Natesh Narain <nnaraindev@gmail.com>
*/

#include <gtest/gtest.h>
#include "test_helper.h"

#include <gameboycore/gameboycore.h>

using namespace gb;

TEST(StackInstructions, PushPop)
{
	// test load immediate for all registers

	CodeGenerator code;
	code.block(
		0x01, 0x34, 0x12,	// LD BC,$1234
		0x11, 0x78, 0x56,	// LD DE,$5678
		0x21, 0xBC, 0x9A,	// LD HL,$9ABC
		
		0xC5,				// PUSH BC
		0xD5,				// PUSH DE
		0xE5,				// PUSH HL

		0x01, 0x00, 0x00,	// LD BC,$0000
		0x11, 0x00, 0x00,	// LD DE,$0000
		0x21, 0x00, 0x00,	// LD HL,$0000

		
		0xE1,				// POP HL
		0xD1,				// POP DE
		0xC1,				// POP BC

		0x76				// halt
	);


	GameboyCore gameboy;
	CPU::Status status = run(gameboy, code.rom());

	EXPECT_EQ(status.bc, 0x1234);
	EXPECT_EQ(status.de, 0x5678);
	EXPECT_EQ(status.hl, 0x9ABC);
	EXPECT_EQ(status.sp, 0xFFFE);
}

TEST(StackInstructions, LoadHLwithSPRelative)
{
	CodeGenerator code;
	code.block(
		0xF8, (uint8_t)-1,	// LD HL,SP+r8

		0x76				// halt
	);


	GameboyCore gameboy;
	CPU::Status status = run(gameboy, code.rom());

	EXPECT_EQ(status.hl, 0xFFFD);
}

TEST(StackInstructions, PopAF)
{
	CodeGenerator code;
	code.block(
		0x3E, 0x45,			// LD A,$45
		0x37,				// SCF
		0xF5,				// PUSH AF
		0xF0, 0xFC,			// LDH A,(FC)
		0xF6, 0x01,			// OR $01
		0xE0, 0xFC,			// LDH (FC),A
		0xF1,				// POP AF
		0x76
	);

	GameboyCore gameboy;
	auto status = run(gameboy, code.rom());

	EXPECT_EQ(status.a, 0x45);
	EXPECT_EQ(status.f, CPU::Flags::C);
}