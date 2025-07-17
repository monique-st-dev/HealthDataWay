document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("dna-right");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    canvas.width = 200;
    canvas.height = window.innerHeight;

    const totalLines = 100; // ← по-дълга ДНК
    const spacing = 10;
    const amplitude = 35; // ← по-широка

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const time = Date.now() * 0.0012;
        const centerX = canvas.width / 2;

        for (let i = 0; i < totalLines; i++) {
            const y = i * spacing;

            const phase = time + i * 0.19;
            const offset = -Math.sin(phase) * amplitude;  // ← обръщаме посоката!

            const xLeft = centerX - offset;
            const xRight = centerX + offset;

            const isEven = i % 2 === 0;
            const leftColor = isEven ? "#ffd76a" : "#a7d8ec";
            const rightColor = isEven ? "#a7d8ec" : "#ffd76a";

            // Линия
            ctx.beginPath();
            ctx.moveTo(xLeft, y);
            ctx.lineTo(xRight, y);
            ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
            ctx.lineWidth = 1;
            ctx.stroke();

            // Точка със сияние
            function drawPoint(x, y, color) {
                ctx.beginPath();
                ctx.arc(x, y, 2, 0, Math.PI * 2);
                ctx.fillStyle = color;
                ctx.shadowColor = color;
                ctx.shadowBlur = 30;
                ctx.fill();
                ctx.shadowBlur = 0;
            }

            drawPoint(xLeft, y, leftColor);
            drawPoint(xRight, y, rightColor);
        }

        requestAnimationFrame(draw);
    }

    draw();
});
