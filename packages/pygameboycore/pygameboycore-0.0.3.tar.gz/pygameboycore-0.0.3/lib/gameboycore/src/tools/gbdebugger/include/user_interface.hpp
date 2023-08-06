#ifndef USER_INTERFACE_H
#define USER_INTERFACE_H

#include "audio_stream.hpp"
#include "frame_buffer.hpp"

#include <SFML/Window.hpp>
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>

#include <gameboycore/gameboycore.h>

#include <functional>
#include <map>

class UserInterface
{
public:
    UserInterface();
    ~UserInterface();

    void initialize(gb::GameboyCore& core);

    void update();

    bool isRunning() const;

    void scanlineCallback(const gb::GPU::Scanline& scanline, int line);
    void vblankCallback();

private:
    void handleKeyPress(sf::Keyboard::Key key);
    void handleKeyRelease(sf::Keyboard::Key key);

    sf::RenderWindow window_;
    sf::Clock delta_clock_;

    sf::RectangleShape screen_rect_;
    sf::Texture screen_texture_;
    Framebuffer<160, 144, 4> framebuffer_;

    AudioStream audio_stream_;

    std::map<sf::Keyboard::Key, gb::Joy::Key> key_map_;
    std::function<void(gb::Joy::Key)> key_press_;
    std::function<void(gb::Joy::Key)> key_release_;
};

#endif