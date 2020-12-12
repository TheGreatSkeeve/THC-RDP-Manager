# THC-RDP-Manager
<h5>This repository contains code for a fairly basic RDP manager, because I've never met an RDP manager I liked.</h5>
<h2>Main Functions</h2>

 * Connect to servers using RDP connection files from the connections/ subdirectory
 * Create RDP files 
   * Encrypts password using Powershell Secure String, saves it in .rdp file
   * Signs RDP file
   * Creates a self signed cert in the Personal cert store if it doesn't exist
   * Copies the self-signed cert to Trusted Root Certificate Authorities if it doesn't exist
   * Updates registry to trust the publisher
 * Delete RDP files
<h2>Improvements</h2>
 * Make Connection Details column better, it only works half the time
 * Enable editing of RDP files instead of creating
 * Add top bar menu
 * Add option to hide console output
 * Generally make UI look prettier
 * Figure out how to separate single clicks from double clicks in PySimpleGUI, so a single click on a connection entry will bring up the details, and a double click will execute it.  

