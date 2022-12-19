#!/usr/bin/env bash

#setxkbmap latam
xset -dpms s off
setxkbmap en_US
numlockx on # Enabale numeric keyboard
blueman-applet & # Blueman APP
/usr/lib/bluetooth/obexd -n & # Sending/Receiving Files From Host/ExternalDevice
pcmanfm -d &
picom -b # Start the compositor - Add transparency to certain windows
nm-applet &
