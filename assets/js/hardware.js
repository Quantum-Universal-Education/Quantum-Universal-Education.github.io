var hardware_strs = ["Trapped Ion", "Quantum Dot", "Superconducting", "Diamond NV and SiV", "Topological", "NMR", "Adiabatic"];
var hardware_ext = [
"jpg",
"",
"png",
"",
"",
"",
"jpg" 
];
var img_srcs = [
"https://en.wikipedia.org/wiki/File:Quantum_Computing;_Ion_Trapping_(5941055642).jpg | public domain",  // public domain
"",
"https://en.wikipedia.org/wiki/Transmon#/media/File:4_Qubit,_4_Bus,_4_Resonator_IBM_Device_(Jay_M._Gambetta,_Jerry_M._Chow,_and_Matthias_Steffen,_2017).png | CC BY 4.0 https://creativecommons.org/licenses/by/4.0/",  // CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
"",
"",
"",
"https://en.wikipedia.org/wiki/D-Wave_Systems#/media/File:DWave_128chip.jpg | CC BY 3.0 https://creativecommons.org/licenses/by/3.0/"  // CC BY 3.0: https://creativecommons.org/licenses/by/3.0/
];

var first = Math.floor(Math.random() * hardware_strs.length);
var html_str = "";
var i;
for (i = 0; i < hardware_strs.length; i++) {
  var idx = (first + i) % hardware_strs.length; 
  // html_str += "<a href=\"https://fullstackquantumcomputation.tech/hardware/\">" + hardware_strs[idx] + "</a><img src=\"/assets/images/areas/hardware/"+hardware_strs[idx]+"."+hardware_ext[idx]+"\"><p style=\"text-align: right; font-size: 8px\"><a href=\"" + img_srcs[idx] + "\">image source</a></p><br>\n";
  // html_str += "<a href=\"https://fullstackquantumcomputation.tech/hardware/\">" + hardware_strs[idx] + "</a><img src=\"/assets/images/areas/hardware/"+hardware_strs[idx]+"."+hardware_ext[idx]+"\"><br>\n";
  // html_str += "<a href=\"https://fullstackquantumcomputation.tech/hardware/\">" + hardware_strs[idx] + "</a><img src=\"/assets/images/areas/hardware/"+hardware_strs[idx]+"."+hardware_ext[idx]+"\"><p style=\"text-align: right; font-size: 8px\"><a href=\"" + img_srcs[idx] + "\">image source</a></p><br>\n";
  html_str += "<div style=\"border: 1px solid black; width: 50vw; padding: 10px; margin: 10px; text-align: center\"><a href=\"https://fullstackquantumcomputation.tech/hardware/\">" + hardware_strs[idx] + "</a><br><img src=\"/assets/images/areas/hardware/"+hardware_strs[idx]+"."+hardware_ext[idx]+"\"><a href=\"" + img_srcs[idx] + "\"><p style=\"text-align:right; font-size:8px;\">image source</p></a></div><br>\n";
}
document.getElementById("hardware").innerHTML = html_str;

