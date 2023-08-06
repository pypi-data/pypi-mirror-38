/**
	Test Load Instructions on CPU
	
	@author Natesh Narain <nnaraindev@gmail.com>
*/

#include <gtest/gtest.h>
#include "test_helper.h"
#include "util/codegenerator.h"

#include <gameboycore/gameboycore.h>

using namespace gb;

TEST(LoadInstructionsTest, Load8BitImmediate)
{
	// test load immediate for all registers

	CodeGenerator code;
	code.block(
		0x3E, 0x01, // LD A,1
		0x06, 0x02, // LD B,2
		0x0E, 0x03, // LD C,3
		0x16, 0x04, // LD D,4
		0x1E, 0x05, // LD E,5
		0x26, 0xC0, // LD H,6
		0x2E, 0x00, // LD L,7
		0x36, 0x08, // LD (HL),$08

		0x76        // halt
	);

	
	GameboyCore gameboy;
	CPU::Status status = run(gameboy, code.rom());
	
	auto& mmu = gameboy.getMMU();

	EXPECT_EQ(status.a, 1);
	EXPECT_EQ(status.b, 2);
	EXPECT_EQ(status.c, 3);
	EXPECT_EQ(status.d, 4);
	EXPECT_EQ(status.e, 5);
	EXPECT_EQ(status.h, 0xC0);
	EXPECT_EQ(status.l, 0x00);
	EXPECT_EQ(mmu->read(status.hl), 0x08);
}

TEST(LoadInstructionsTest, Load16BitImmediate)
{
	// test load immediate for all registers

	CodeGenerator code;
	code.block(
		0x01, 0x34, 0x12, // LD BC,$1234
		0x11, 0x78, 0x56, // LD DE,$5678
		0x21, 0xBC, 0x9A, // LD HL,$9ABC
		0x31, 0xFE, 0xFF, // LD SP,$FFFE

		0x76              // halt
	);

	
	GameboyCore gameboy;
	CPU::Status status = run(gameboy, code.rom());
	
	EXPECT_EQ(status.bc, 0x1234);
	EXPECT_EQ(status.de, 0x5678);
	EXPECT_EQ(status.hl, 0x9ABC);
	EXPECT_EQ(status.sp, 0xFFFE);
}

TEST(LoadInstructionsTest, Transfer)
{
	CodeGenerator code;
	code.block(
		0x06, 0x05, // LD B,5
		0x50,		// LD D,B
		0x60,		// LD H,B

		0x76
	);

	GameboyCore gameboy;
	CPU::Status status;
	
	status = run(gameboy, code.rom());

	EXPECT_EQ(status.d, 0x05);
	EXPECT_EQ(status.h, 0x05);

	code.reset();
	code.block(
		0x0E, 0x03, // LD C,3
		0x41,		// LD B,C
		0x51,		// LD D,C
		0x61,		// LD H,C

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.b, 0x03);
	EXPECT_EQ(status.d, 0x03);
	EXPECT_EQ(status.h, 0x03);

	code.reset();
	code.block(
		0x16, 0x04, // LD D,4
		0x42,		// LD B,D
		0x62,		// LD H,D

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.b, 0x04);
	EXPECT_EQ(status.h, 0x04);

	code.reset();
	code.block(
		0x1E, 0x06, // LD E,6
		0x43,		// LD B,E
		0x53,		// LD D,E
		0x62,		// LD H,E

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.b, 0x06);
	EXPECT_EQ(status.d, 0x06);
	EXPECT_EQ(status.h, 0x06);

	code.reset();
	code.block(
		0x26, 0x07, // LD H,7
		0x44,		// LD B,H
		0x54,		// LD D,H

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.b, 0x07);
	EXPECT_EQ(status.d, 0x07);

	code.reset();
	code.block(
		0x2E, 0x08, // LD L,8
		0x45,		// LD B,L
		0x55,		// LD D,L
		0x65,		// LD H,L

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.b, 0x08);
	EXPECT_EQ(status.d, 0x08);
	EXPECT_EQ(status.h, 0x08);

	code.reset();
	code.block(
		0x3E, 0x09, // LD A,9
		0x47,		// LD B,A
		0x57,		// LD D,A
		0x67,		// LD H,A

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.b, 0x09);
	EXPECT_EQ(status.d, 0x09);
	EXPECT_EQ(status.h, 0x09);

	code.reset();
	code.block(
		0x06, 0x0A, // LD B,$A
		0x48,		// LD C,B
		0x58,		// LD E,B
		0x68,		// LD L,B
		0x78,		// LD A,B

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.c, 0x0A);
	EXPECT_EQ(status.e, 0x0A);
	EXPECT_EQ(status.l, 0x0A);
	EXPECT_EQ(status.a, 0x0A);

	code.reset();
	code.block(
		0x0E, 0x0B, // LD C,$B
		0x59,		// LD E,C
		0x69,		// LD L,C
		0x79,		// LD A,C

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.e, 0x0B);
	EXPECT_EQ(status.l, 0x0B);
	EXPECT_EQ(status.a, 0x0B);

	code.reset();
	code.block(
		0x16, 0x0C, // LD D,$C
		0x4A,		// LD C,D
		0x5A,		// LD E,D
		0x6A,		// LD L,D
		0x7A,		// LD A,D

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.c, 0x0C);
	EXPECT_EQ(status.e, 0x0C);
	EXPECT_EQ(status.l, 0x0C);
	EXPECT_EQ(status.a, 0x0C);

	code.reset();
	code.block(
		0x1E, 0x0D, // LD E,$D
		0x4B,		// LD C,E
		0x6B,		// LD L,E
		0x7B,		// LD A,E

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.c, 0x0D);
	EXPECT_EQ(status.l, 0x0D);
	EXPECT_EQ(status.a, 0x0D);

	code.reset();
	code.block(
		0x26, 0x0E, // LD H,$E
		0x4C,		// LD C,H
		0x5C,		// LD E,H
		0x6C,		// LD L,H
		0x7C,		// LD A,H

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.c, 0x0E);
	EXPECT_EQ(status.e, 0x0E);
	EXPECT_EQ(status.l, 0x0E);
	EXPECT_EQ(status.a, 0x0E);

	code.reset();
	code.block(
		0x2E, 0x0F, // LD L,$F
		0x4D,		// LD C,L
		0x5D,		// LD E,L
		0x7D,		// LD A,L

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.c, 0x0F);
	EXPECT_EQ(status.e, 0x0F);
	EXPECT_EQ(status.a, 0x0F);

	code.reset();
	code.block(
		0x3E, 0x01, // LD A,$F
		0x4F,		// LD C,A
		0x5F,		// LD E,A
		0x6F,		// LD L,A

		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.c, 0x01);
	EXPECT_EQ(status.e, 0x01);
	EXPECT_EQ(status.l, 0x01);
}

TEST(LoadInstructionsTest, LoadRegisterFromMemory)
{
	CodeGenerator code;
	code.block(
		0x21, 0x50, 0x02,	// LD HL,$0250
		0x46,				// LD B,(HL)
		0x56,				// LD D,(HL)
		0x4E,				// LD C,(HL)
		0x5E,				// LD E,(HL)
		0x7E,				// LD A,(HL)
		0x66,				// LD H,(HL)

		0x76
	);

	code.address(0x250);
	code.block(0xAE);

	GameboyCore gameboy;
	CPU::Status status;

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.b, 0xAE);
	EXPECT_EQ(status.c, 0xAE);
	EXPECT_EQ(status.d, 0xAE);
	EXPECT_EQ(status.e, 0xAE);
	EXPECT_EQ(status.a, 0xAE);

	EXPECT_EQ(status.h, 0xAE);
}

TEST(LoadInstructionsTest, LoadMemoryFromRegister)
{
	GameboyCore gameboy;
	
	CPU::Status status;
	MMU::Ptr* mmu;

	CodeGenerator code;

	code.block(
		0x21, 0x00, 0xC0,	// LD HL, $250
		0x06, 0x05,			// LD B,5
		0x70,				// LD (HL),B

		0x76
	);
	status = run(gameboy, code.rom());
	mmu = &gameboy.getMMU();

	EXPECT_EQ((*mmu)->read(0xC000), 0x05);

	code.reset();
	code.block(
		0x21, 0x01, 0xC0,	// LD HL, $251
		0x0E, 0x05,			// LD C,5
		0x71,				// LD (HL),C

		0x76
	);
	status = run(gameboy, code.rom());
	mmu = &gameboy.getMMU();

	EXPECT_EQ((*mmu)->read(0xC001), 0x05);

	code.reset();
	code.block(
		0x21, 0x02, 0xC0,	// LD HL, $252
		0x16, 0x05,			// LD D,5
		0x72,				// LD (HL),D

		0x76
	);
	status = run(gameboy, code.rom());
	mmu = &gameboy.getMMU();

	EXPECT_EQ((*mmu)->read(0xC002), 0x05);

	code.reset();
	code.block(
		0x21, 0x03, 0xC0,	// LD HL, $253
		0x1E, 0x05,			// LD E,5
		0x73,				// LD (HL),E

		0x76
	);
	status = run(gameboy, code.rom());
	mmu = &gameboy.getMMU();

	EXPECT_EQ((*mmu)->read(0xC003), 0x05);
}

TEST(LoadInstructionsTest, LoadMemoryIncDec)
{
	GameboyCore gameboy;
	CPU::Status status;

	CodeGenerator code;

	code.block(
		0x3E, 0x05,			// LD A,5
		0x21, 0x00, 0xC0,	// LD HL,$250
		0x22,				// LD (HL+1),A
		0x3E, 0x06,			// LD A,6
		0x32,				// LD (HL-1),A

		0x76
	);

	status = run(gameboy, code.rom());
	auto& mmu = gameboy.getMMU();

	EXPECT_EQ(status.a, 6);
	EXPECT_EQ(status.hl, 0xC000);
	EXPECT_EQ(mmu->read(0xC000), 5);
	EXPECT_EQ(mmu->read(0xC001), 6);
}

TEST(LoadInstructionsTest, LoadRegisterIncDec)
{
	GameboyCore gameboy;
	CPU::Status status;

	CodeGenerator code;

	code.block(
		0x21, 0x50, 0x02,	// LD HL,$250
		0x2A,				// LD A,($250 + 1)

		0x76
	);
	code.address(0x250);
	code.block(0x06);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.a, 6);
	EXPECT_EQ(status.hl, 0x251);

	code.reset();
	code.block(
		0x21, 0x50, 0x02,	// LD HL,$250
		0x3A,				// LD A,($250 - 1)

		0x76
	);
	code.address(0x24F);
	code.block(0x06);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.a, 6);
	EXPECT_EQ(status.hl, 0x24F);
}

TEST(LoadInstructionsTest, In) 
{
	GameboyCore gameboy;
	CPU::Status status;

	CodeGenerator code;

	code.block(
		0x21, 0x05, 0xFF,	// LD HL,$FF05
		0x06, 0xFE,			// LD B,$FE
		0x70,				// LD (HL),B
		0x0E, 0x05,			// LD C,5

		0xF2,				// LD A,(C)
		
		0x76
	);

	status = run(gameboy, code.rom());

	EXPECT_EQ(status.a, 0xFE);
}

TEST(LoadInstructionsTest, Out)
{
	GameboyCore gameboy;
	CPU::Status status;

	CodeGenerator code;

	code.block(
		0x0E, 0x05,			// LD C,5
		0x3E, 0xFF,			// LD A,$FF

		0xE2,				// LD (C),A

		0x76
	);

	status = run(gameboy, code.rom());
	auto& mmu = gameboy.getMMU();

	EXPECT_EQ(mmu->read(0xFF05), 0xFF);
}