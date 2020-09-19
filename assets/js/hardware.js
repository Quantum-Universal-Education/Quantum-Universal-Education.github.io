var hardware_strs = ["Trapped Ion", "Quantum Dot", "Superconducting", "Diamond NV and SiV", "Topological", "NMR", "Adiabatic", "Photonic", "Neutral Atoms and Molecules"];
var hardware_ext = [
"jpg",
"jpg",
"png",
"jpg",
"PNG",
"gif",
"jpg",
"png",
"png"
];
var img_srcs = [
"https://en.wikipedia.org/wiki/File:Quantum_Computing;_Ion_Trapping_(5941055642).jpg",  // public domain
"https://en.wikipedia.org/wiki/File:QD_S.jpg", // CC BY-SA 3.0: https://creativecommons.org/licenses/by-sa/3.0/deed.en
"https://en.wikipedia.org/wiki/Transmon#/media/File:4_Qubit,_4_Bus,_4_Resonator_IBM_Device_(Jay_M._Gambetta,_Jerry_M._Chow,_and_Matthias_Steffen,_2017).png",  // CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
"https://en.wikipedia.org/wiki/Nitrogen-vacancy_center#/media/File:Model_of_nitrogen-vacancy_center_in_diamond.jpg", // CC BY-SA 3.0: https://creativecommons.org/licenses/by-sa/3.0/
"https://artbyphysicistkittyyeung.com/2020/05/24/quantum-computing-through-comics/#jp-carousel-3485", // CC BY-NC-SA 4.0: https://creativecommons.org/licenses/by-nc-sa/4.0/ This image is a cropped version of the original under CC BY-NC-SA 4.0 linked with permission of Kitty Yeung
"https://en.wikipedia.org/wiki/Nuclear_magnetic_resonance#/media/File:NMR_EPR.gif", // CC BY-SA 3.0: https://creativecommons.org/licenses/by-sa/3.0/
"https://en.wikipedia.org/wiki/D-Wave_Systems#/media/File:DWave_128chip.jpg",  // CC BY 3.0: https://creativecommons.org/licenses/by/3.0/
"https://en.wikipedia.org/wiki/Optical_computing#/media/File:Optical-NOT-gate-int.svg", // CC0 1.0: https://creativecommons.org/publicdomain/zero/1.0/deed.en
"https://physicstoday.scitation.org/doi/10.1063/PT.3.3626"
];

var first = Math.floor(Math.random() * hardware_strs.length);
var html_str = "";
var i;
for (i = 0; i < hardware_strs.length; i++) {
  var idx = (first + i) % hardware_strs.length; 
  html_str += "<div style=\"border: 1px solid black; width: 50vw; padding: 10px; margin: 10px; text-align: center\"><a href=\"/hardware/" + hardware_strs[idx].replace(/ /g, "-") + "/\">" + hardware_strs[idx] + "</a><br><img src=\"/assets/images/areas/hardware/"+hardware_strs[idx]+"."+hardware_ext[idx]+"\" style=\"width: 30vw\"><a href=\"" + img_srcs[idx] + "\"><p style=\"text-align:right; font-size:8px;\">image source</p></a></div><br>\n";
}
document.getElementById("hardware").innerHTML = html_str;

