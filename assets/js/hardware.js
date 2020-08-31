---
permalink: /hardware/
title: "Quantum Hardware"
---

var hardware_strs = ["Trapped Ion", "Quantum Dot", "Superconducting", "Diamond NV and SiV", "Topological", "NMR", "Adiabatic"];
var hardware_ext = [
"jpg", //  src: https://en.wikipedia.org/wiki/File:Quantum_Computing;_Ion_Trapping_(5941055642).jpg | public domain
"",
"png", //  src: https://en.wikipedia.org/wiki/Transmon#/media/File:4_Qubit,_4_Bus,_4_Resonator_IBM_Device_(Jay_M._Gambetta,_Jerry_M._Chow,_and_Matthias_Steffen,_2017).png | CC BY 4.0 https://creativecommons.org/licenses/by/4.0/
"",
"",
"",
"jpg" //  src: https://en.wikipedia.org/wiki/D-Wave_Systems#/media/File:DWave_128chip.jpg | CC BY 3.0 https://creativecommons.org/licenses/by/3.0/
];

var first = Math.floor(Math.random() * hardware_strs.length);
var html_str = "";
var i;
for (i = 0; i < hardware_strs.length; i++) {
  var idx = (first + i) % hardware_strs.length;
  html_str += "<a href=\"https://fullstackquantumcomputation.tech/hardware/\"><img src=\"/assets/images/areas/hardware/"+hardware_strs[idx]+"."+hardware_ext[idx]+"\">"+hardware_strs[idx]+"</a>\n";
}
document.getElementById("hardware").innerHTML = html_str;

