const createBuffsLineGraph = (data, graphId, title, colour, awakening = false, awakeningTriggers = null) => {
    const buffCountData = data;
    const buffCountDataArray = Object.keys(buffCountData).map(key => ({ key: +key, value: buffCountData[key] }));

    const margin = { top: 60, right: 20, bottom: 55, left: 65 },
        width = 600 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom;

    const svgContainer = d3.select(graphId).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("background", "transparent");

    const svg = svgContainer.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    svg.append("text")
        .attr("x", width / 2)
        .attr("y", -26)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("fill", "white")
        .text(`${title} Count`);

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
        .domain(d3.extent(buffCountDataArray, d => d.key))
        .range([0, width]);
        
    const y = d3.scaleLinear()
        .domain([0, d3.max(buffCountDataArray, d => d.value)])
        .range([height, 0]);

    const line = d3.line()
        .x(d => x(d.key))
        .y(d => y(d.value))
        .curve(d3.curveMonotoneX);

    svg.append("path")
        .datum(buffCountDataArray)
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
        .attr("y", 41)
        .style("text-anchor", "middle")
        .text("Time");

    xAxisGroup.selectAll("line").style("stroke", "white");
    xAxisGroup.selectAll("path").style("stroke", "white");
    xAxisGroup.selectAll("text").style("fill", "white");

    const yAxisGroup = svg.append("g")
        .call(d3.axisLeft(y));

    yAxisGroup.append("text")
        .attr("class", "axis-label")
        .attr("transform", "rotate(-90)")
        .attr("x", -height / 2)
        .attr("y", -35)
        .style("text-anchor", "middle")
        .text("Count");

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
            const count = buffCountData[`${Math.round(x.invert(adjustedMouseX))}`];

            tooltip.html(`<span class="tooltip-time">${time}</span><br/>
                        <span class="tooltip-count" style="color: ${colour}">${Math.round(count * 10) / 10}</span>`)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 15) + "px")
                .style("opacity", 1);
        } else {
            tooltip.style("opacity", 0);
        };
    })
    .on("mouseout", function() { 
        tooltip.style("opacity", 0);
    });
    
    // disastrous attempt at plotting most common points for awakening to reach 12 stacks
    function findPeakIntervals(data, cooldownPeriod, iterations) {
        let interval = 65;
        let previousPeak = 0;
        let peaks = [];
        
        const encounterLength = Number(document.getElementById("encounter-length-option").value);
    
        while (previousPeak <= encounterLength) {
            // console.log(`Checking between ${previousPeak} and ${interval}`);
    
            let filteredEntries = Object.entries(data)
                .filter(([key, _]) => Number(key) <= interval && Number(key) > previousPeak + cooldownPeriod);
    
            if (filteredEntries.length === 0) {
                interval += 65;
                if (interval > encounterLength) {
                    break;
                };
                continue;
            };
    
            let highestValueEntry = filteredEntries.reduce((prev, current) => {
                return (prev[1] > current[1]) ? prev : current;
            }, [null, -Infinity]);
    
            let keyWithHighestValue = Number(highestValueEntry[0]);

            // console.log(highestValueEntry[1])
            // console.log(iterations * 0.03)

            if (highestValueEntry[1] >= iterations * 0.01) {
                peaks.push({ key: keyWithHighestValue });
            };
            
            // console.log("Highest key", keyWithHighestValue);
    
            previousPeak = keyWithHighestValue;
            interval = keyWithHighestValue + Math.max(65, keyWithHighestValue - previousPeak);
    
            // console.log("New interval", interval);
        };
        return peaks;
    };
    
    if (awakening) {
        const cooldownPeriod = 30;
        const iterations = document.getElementById("iterations-option").value;
        const peaks = findPeakIntervals(awakeningTriggers, cooldownPeriod, iterations);

        peaks.forEach(point => {
            svg.append("line")
                .attr("x1", x(point.key))
                .attr("x2", x(point.key))
                .attr("y1", y(point.value))
                .attr("y2", height)
                .attr("stroke", "var(--healing-font)")
                .attr("stroke-width", 1);
        });
    };
    
    return svg;
};

export { createBuffsLineGraph };