var left_img_creds = [
"Left image drawn by Lia Yeh.  Quantum Universal Education.  Open-sourced under ECL-2.0 license",
"Left image concept by Samanvay Sharma and drawn by Alberto Maldonado Romo.  Quantum Universal Education.  Open-sourced under ECL-2.0 license",
"Left image drawn by Lia Yeh.  Quantum Universal Education.  Open-sourced under ECL-2.0 license",
"Left image drawn by Lia Yeh.  Quantum Universal Education.  Open-sourced under ECL-2.0 license",
"Left image drawn by Alberto Maldonado Romo.  Quantum Universal Education.  Open-sourced under ECL-2.0 license",
"Left image drawn by Alberto Maldonado Romo.  Quantum Universal Education.  Open-sourced under ECL-2.0 license",
"Left image drawn by Lia Yeh.  Quantum Universal Education.  Open-sourced under ECL-2.0 license",
"Left image drawn by Jayanti Singh and Hemant Chaurasia.  Quantum Universal Education.  Open-sourced under ECL-2.0 license",
"Left image drawn by Alberto Maldonado Romo.  Quantum Universal Education.  Open-sourced under ECL-2.0 license"];
var left_img_srcs = [
"ions",
"nmr",
"diamond_nv",
"neutral_atoms",
"photonic",
"superconducting",
"topological",
"cQED",
"dot"];
var right_img_srcs = [
"https://olv.duke.edu/news/ionq-raises-additional-funding-for-its-quantum-computing-platform/",
"http://www.org.chemie.tu-muenchen.de/glaser/qcomp.html",
"https://phys.org/news/2019-05-quantum-technologies-materials-atomic-scale.html",
"https://physicstoday.scitation.org/doi/10.1063/PT.3.3626",
"https://spectrum.ieee.org/tech-talk/computing/hardware/photonic-quantum",
"https://www.news.ucsb.edu/2016/017014/entanglement-chaos",
"https://physicstoday.scitation.org/doi/full/10.1063/PT.3.4499",
"https://www.ase.sci.waseda.ac.jp/update/closeup_en/1254",
"https://www.nersc.gov/news-publications/nersc-news/science-news/2015/quantum-dot-blinking/"];
var def_srcs = [
"https://arxiv.org/pdf/quant-ph/9608011.pdf",
"https://link.springer.com/chapter/10.1007%2F978-0-387-75714-8_14",
"https://phys.org/news/2019-05-quantum-technologies-materials-atomic-scale.html",
"https://physicstoday.scitation.org/doi/10.1063/PT.3.3626",
"https://spectrum.ieee.org/tech-talk/computing/hardware/photonic-quantum",
"https://www.nature.com/articles/s41586-019-1666-5",
"https://physicstoday.scitation.org/doi/full/10.1063/PT.3.4499",
"https://www.ase.sci.waseda.ac.jp/update/closeup_en/1254",
"https://www.nersc.gov/news-publications/nersc-news/science-news/2015/quantum-dot-blinking/"];

var first = Math.floor(Math.random() * right_img_srcs.length);
var html_str = "";
var i;
for (i = 0; i < left_img_srcs.length; i++) {
  var idx = (first + i) % left_img_srcs.length; 
  html_str += "<div style=\"border: 0px solid black; width: 65vw; padding: 0px; margin: 0px; text-align: center\"><a href=\"/hardware/" + left_img_srcs[idx] + "/\"><img src=\"/assets/images/hardwares/"+"Slide"+(idx+1)+".PNG"+"\" style=\"width: 65vw\"></a><a href=\"" + "/assets/images/hardwares/" + left_img_srcs[idx] + ".svg" + "\"><p style=\"text-align:right; font-size:8px;\">" + left_img_creds[idx] + "</p></a><a href=\"" + right_img_srcs[idx] + "\"><p style=\"text-align:right; font-size:8px;\">right image source</p></a><a href=\"" + def_srcs[idx] + "\"><p style=\"text-align:right; font-size:8px;\">definition source</p></a></div><br>\n";
}
document.getElementById("hardware").innerHTML = html_str;

