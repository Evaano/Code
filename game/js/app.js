const canvas = document.querySelector('canvas')

const context = canvas.getContext('2d')

context.fillStyle = 'white'
context.fillRect(0, 0, canvas.width, canvas.height)

const image = new Image()
image.src = './images/map.png'

console.log(image)

image.onload = () => {
    context.drawImage(image, -100, -10023 )
}