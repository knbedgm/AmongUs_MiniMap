let stage, iconLayer, mapLayer, line, socket

let currentMap = 0;

var players = {}
var playerIcons = {}

function main() {
  stage = new Konva.Stage({
    container: 'container',   // id of container <div>
    width: 1920,
    height: 1080
  });
  iconLayer = new Konva.Layer();
  mapLayer = new Konva.Layer();

  // create our shape
  line1 = new Konva.Line({
    points: [],
    stroke: 'black',
    strokeWidth: 100,
    lineJoin: "round",
    lineCap: "round",
  });

  line2 = new Konva.Line({
    points: [],
    stroke: 'red',
    strokeWidth: 100,
    lineJoin: "round",
    lineCap: "round",
  });

  // add the shape to the layer
  iconLayer.add(line1);
  iconLayer.add(line2);

  // add the layer to the stage
  stage.add(mapLayer);
  stage.add(iconLayer);

  // draw the image
  iconLayer.draw();

  // map setup 
  setMap(currentMap)

  //   addPoint(50,50);
  //   addPoint(500,500);
  i = 0
  //   setInterval(() => {if (i>359) {i=0} else {i+=5} line.attrs.stroke = "hsl("+i+", 100%, 50%)", iconLayer.draw()}, 50)

  socket = io()

  socket.on("movement", a => {
    players[a.id] = a
    draw()

    if (a.id == 6) {
      let { x, y } = a
      addPoint(x, y, 1)
    } else if (a.id == 60) {
      let { x, y } = a
      addPoint(x, y, 2)
    }
  })


  socket.on("changeMap", a=> {
    setMap(a.id)
  })
}

function map(OldMin, OldMax, NewMin, NewMax, OldValue) {
  return (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

}

function mapXY(xy, set) {
  let mapers = [
    [[48, -500], [-48, 1000]],
    [[48, -500], [-48, 1000]],
    [[48, -500], [-48, 1000]],
  ]
  return {
    x: (xy.x / mapers[set][0][0] + mapers[set][0][1]),
    y: (xy.y / mapers[set][1][0] + mapers[set][1][1]),
  }

}

function addPoint(x, y, n) {
  let tailLen = 500
  if (n == 1) {
    line1.attrs.points = line1.attrs.points.concat([x, y])
    if (line1.attrs.points.length > tailLen) {
      line1.attrs.points = line1.attrs.points.slice(2, tailLen + 2)
    }
  } else if (n == 2) {
    line2.attrs.points = line2.attrs.points.concat([x, y])
    if (line2.attrs.points.length > tailLen) {
      line2.attrs.points = line2.attrs.points.slice(2, tailLen + 2)
    }
  }
  iconLayer.draw()
}

function doTransform() {
  let transforms = [
    {
      x: -330,
      y: 1125,
      scaleX: 1 / 35.5,
      scaleY: 1 / -35.5,
    },
    {
      x: -480,
      y: 1280,
      scaleX: 1 / 44,
      scaleY: 1 / -44,
    },
    {
      x: -775,
      y: 915,
      scaleX: 1 / 40,
      scaleY: 1 / -40,
    }
  ]
  iconLayer.setAttrs(transforms[currentMap])
  iconLayer.draw();
}

function draw() {
  doTransform()
  for (let i in players) {
    let player = players[i];
    if (playerIcons[i] == null) {
      playerIcons[i] = new Konva.Circle(_.merge({
        radius: 500,
        fill: 'gray',
        stroke: 'black',
        strokeWidth: 200
      }, _.pick(player, ['x', 'y'])));
      iconLayer.add(playerIcons[i]);
    }
    new Konva.Tween(_.merge({
      node: playerIcons[i],
      duration: 0.25,
    }, _.pick(player, ['x', 'y']))).play();
  }
  iconLayer.batchDraw()
}

function setMap(mdex) {
  if (mdex < 0 || mdex > 2) {
    return
  }

  currentMap = mdex
  let uri = ""

  switch (mdex) {
    case 0:
      uri = "/maps/skeld.png"
      break;
    case 1:
      uri = "/maps/mirahq.png"
      break;
    case 2:
      uri = "/maps/polus.png"
      break;
    default:
      break;
  }
  Konva.Image.fromURL(uri, function (img) {
    img.setAttrs({
      x: 50,
      y: 50,
    });
    mapLayer.destroyChildren()
    mapLayer.add(img);
    mapLayer.batchDraw();
  });

  doTransform()

}

function erase() {
  players = []
  iconLayer.destroyChildren()
  playerIcons = []
  draw()
}