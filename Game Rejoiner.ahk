#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

^+g::
CoordMode, Mouse, Client

KeyWait, f, d
KeyWait, f

Loop 5 {
Gosub GoGame
}
Msgbox Done
return

^+!g::
CoordMode, Mouse, Client

KeyWait, f, d
KeyWait, f

Loop 40 {
Gosub GoGame
}
Msgbox, Done
return

GoGame:
Click, 477, 545 ; Click game code box
Send CLBKFF
Sleep, 200
Click, 620, 545 ; Click go button

Sleep 6000

if(GetKeystate("f")) {
Msgbox Exit
Exit
}

Click, 915, 40 ; Click settings button
Sleep, 600
Click, 475, 475
Sleep, 600

if(GetKeystate("f")) {
Msgbox Exit
Exit
}
return