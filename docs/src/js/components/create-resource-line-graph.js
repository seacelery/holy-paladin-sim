import { formatNumbers } from './index.js';

const createResourceGraph = (data, graphId, title, colour) => {
    const dataArray = Object.keys(data).map(key => ({ key: +key, value: data[key] }));
    
    const margin = { top: 30, right: 30, bottom: 75, left: title === "Mana" ? 75 : 45 },
        width = 640 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    const svgContainer = d3.select(graphId).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("background", "transparent");

    const svg = svgContainer.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const formatTime = (seconds) => {
        let minutes = Math.floor(seconds / 60);
        let remainingSeconds = Math.round(seconds % 60);

        if (remainingSeconds === 60) {
            minutes += 1;
            remainingSeconds = 0;
        };
    
        return [minutes, remainingSeconds].map(t => String(t).padStart(2, '0')).join(':');
    };

    const x = d3.scaleLinear()
        .domain(d3.extent(dataArray, d => d.key))
        .range([0, width]);
        
        const y = d3.scaleLinear()
        .domain(title === "Holy Power" ? [0, 5] : [0, d3.max(dataArray, d => d.value)])
        .range([height, 0]);

    const line = d3.line()
        .x(d => x(d.key))
        .y(d => y(d.value))
        .curve(d3.curveMonotoneX);

    svg.append("path")
        .datum(dataArray)
        .attr("fill", "none")
        .attr("stroke", `${colour}`)
        .attr("stroke-width", 1.5)
        .attr("d", line);

    const xAxisGroup = svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x).tickFormat(d => formatTime(d)));

    xAxisGroup.append("text")
        .attr("class", "axis-label")
        .attr("x", (width / 2) - 10)
        .attr("y", 51)
        .style("text-anchor", "middle")
        .text("Time");

    xAxisGroup.selectAll("line").style("stroke", "white");
    xAxisGroup.selectAll("path").style("stroke", "white");
    xAxisGroup.selectAll("text").style("fill", "white");

    const yAxisGroup = svg.append("g")
    .call(d3.axisLeft(y).ticks(title === "Holy Power" ? 5 : 6));

    yAxisGroup.append("text")
        .attr("class", "axis-label")
        .attr("transform", "rotate(-90)")
        .attr("x", -height / 2)
        .attr("y", title === "Mana" ? -60 : -30)
        .style("text-anchor", "middle")
        .text(title);

    yAxisGroup.selectAll("line").style("stroke", "white");
    yAxisGroup.selectAll("path").style("stroke", "white");
    yAxisGroup.selectAll("text").style("fill", "white");

    const tooltip = d3.select(graphId)
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("border-width", "1px")
        .style("border-radius", "3px")
        .style("padding", "5px");

    svgContainer.on("mousemove", function(event) {
        const [mouseX, mouseY] = d3.pointer(event);

        const adjustedMouseX = mouseX - margin.left;
        const adjustedMouseY = mouseY - margin.top;

        if (adjustedMouseX >= 0 && adjustedMouseX <= width && adjustedMouseY >= 0 && adjustedMouseY <= height) {
            const time = formatTime(x.invert(adjustedMouseX));
            const resource = data[`${Math.round(x.invert(adjustedMouseX))}`];

            tooltip.html(`<span class="tooltip-time">${time}</span><br/>
                <span id="tooltip-${title.toLowerCase().replaceAll(" ", "-")}">${title === "Mana" ? formatNumbers(resource) : Math.round(resource * 10) / 10}</span>`)
            .style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY - 15) + "px")
            .style("opacity", 1)
        } else {
            tooltip.style("opacity", 0);
        };
    })
    .on("mouseout", function() { 
        tooltip.style("opacity", 0);
    });

    return svg;
};

export { createResourceGraph };