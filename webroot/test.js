var canvas = document.getElementById('main');
var ctx = canvas.getContext('2d');

const width = canvas.width
const height = canvas.height

ctx.fillStyle = 'rgb(200, 0, 0)';
ctx.fillRect(0, height / 2, width, height / 2);

ctx.fillStyle = 'rgba(0, 0, 200, 0.5)';
ctx.fillRect(0, 0, width, height / 2);

// var myImageData = ctx.createImageData(1, 1);

function getColorForCoord(x, y, data) {
  var red = y * (data.width * 4) + x * 4;
  return [data[red], data[red + 1], data[red + 2], data[red + 3]];
}

function setColorForCoord(x, y, data, colors) {
  var red = y * (data.width * 4) + x * 4;
  data[red] = colors[0];
  data[red + 1] = colors[1];
  data[red + 2] = colors[2];
  data[red + 3] = colors[3];

}


// for (let x = 0; x < width; x++) {
//   for (let y = 0; y < height; y++) {
//     // setColorForCoord(x, y, myImageData, [(x / width) * 255, (y / height) * 255, 0, 255])
//     myImageData[0] = x
//     myImageData[1] = y
//     myImageData[2] = 0
//     myImageData[3] = 255
//     ctx.putImageData(myImageData, x, y);
//   }
// }

//ctx.putImageData(myImageData, 0, 0);

var img = new Image();
//img.source = "/map_skeld.png"


const socket = io()

socket.on("movement", a => {
  socket.emit("ack", a.count)
  console.log(a)
});