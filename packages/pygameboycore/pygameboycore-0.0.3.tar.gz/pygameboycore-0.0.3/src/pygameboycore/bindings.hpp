#pragma once

#include <array>
#include <fstream>
#include <functional>
#include <gameboycore/gameboycore.h>
#include <ios>
#include <iostream>
#include <string>
#include <vector>

const uint8_t GB_WIDTH = 160;
const uint8_t GB_HEIGHT = 144;

using Framebuffer = std::array<uint8_t, GB_WIDTH * GB_HEIGHT * 3>;

class PyGameboyCore : public gb::GameboyCore
{
public:
  enum class KeyAction
  {
      PRESS, RELEASE
  };

  PyGameboyCore()
    : framebuffer_()
  {
  }

  void register_vblank_callback(
      const std::function<void(const Framebuffer&)>& vblank_callback
      )
  {
    getGPU()->setRenderCallback(
      [&](const gb::GPU::Scanline& scanline, int line)
      {
        scanline_callback_(scanline, line);
      }
    );
    vblank_callback_ = vblank_callback;
  }

  void input(gb::Joy::Key key, KeyAction action)
  {
      if(action == KeyAction::PRESS)
      {
          getJoypad()->press(key);
      }
      else
      {
          getJoypad()->release(key);
      }
  }

  void open(const std::string& rom_file)
  {
      std::ifstream file(rom_file, std::ios::binary | std::ios::ate);
      auto size = file.tellg();

      std::vector<uint8_t> buffer;
      buffer.resize(size);

      file.seekg(0, std::ios::beg);
      file.read((char*)&buffer[0], size);

      loadROM(&buffer[0], size);
  }

private:
  void scanline_callback_(const gb::GPU::Scanline& scanline, int line)
  {
    uint32_t i = line * GB_WIDTH * 3;
    for (const auto& pixel : scanline)
    {
      framebuffer_[i+0] = pixel.r;
      framebuffer_[i+1] = pixel.g;
      framebuffer_[i+2] = pixel.b;
      i += 3;
    }

    if (line == 143)
    {
      vblank_callback_(framebuffer_);
    }
  }

private:
  Framebuffer framebuffer_;
  std::function<void(const Framebuffer&)> vblank_callback_;
};
