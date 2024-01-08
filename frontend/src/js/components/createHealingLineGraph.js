const createHealingLineGraph = (healingData, manaData, graphId, title, colour) => {
    const healingDataArray = Object.keys(healingData).map(key => ({ key: +key, value: healingData[key] }));
    const manaDataArray = Object.keys(manaData).map(key => ({ key: +key, value: manaData[key] }));

    const margin = { top: 30, right: 15, bottom: 75, left: 15 },
        width = 1250 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    const svg = d3.select(graphId)
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

    svg.append("text")
        .attr("x", width / 2)
        .attr("y", -26)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("fill", "white")

    const x = d3.scaleLinear()
        .domain(d3.extent(healingDataArray, d => d.key))
        .range([0, width]);
        
    const y = d3.scaleLinear()
        .domain([0, d3.max(healingDataArray, d => d.value)])
        .range([height, 0]);

    const line = d3.line()
        .x(d => x(d.key))
        .y(d => y(d.value))
        .curve(d3.curveMonotoneX);

    svg.append("path")
        .datum(healingDataArray)
        .attr("fill", "none")
        .attr("stroke", `${colour}`)
        .attr("stroke-width", 1.5)
        .attr("d", line);

    const xAxisGroup = svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

    xAxisGroup.append("text")
        .attr("class", "axis-label")
        .attr("x", (width / 2) - 10)
        .attr("y", 51)
        .style("text-anchor", "middle")
        .text("Time");

    xAxisGroup.selectAll("line").style("stroke", "white");
    xAxisGroup.selectAll("path").style("stroke", "white");
    xAxisGroup.selectAll("text").style("fill", "white");

    // left y-axis
    // const yAxisGroup = svg.append("g")
    //     .call(d3.axisLeft(y));

    // yAxisGroup.append("text")
    //     .attr("class", "axis-label")
    //     .attr("transform", "rotate(-90)")
    //     .attr("x", -height / 2)
    //     .attr("y", -70)
    //     .style("text-anchor", "middle")
    //     .text("Healing");

    // yAxisGroup.selectAll("line").style("stroke", "white");
    // yAxisGroup.selectAll("path").style("stroke", "white");
    // yAxisGroup.selectAll("text").style("fill", "white");

    const yRight = d3.scaleLinear()
        .domain([0, d3.max(manaDataArray, d => d.value)])
        .range([height, 0]);

    // right y-axis
    // const yAxisRight = d3.axisRight(yRight);

    // svg.append("g")
    //     .attr("transform", `translate(${width}, 0)`)
    //     .call(yAxisRight)
    //     .selectAll("text")
    //     .style("fill", "white");

    // Path for mana data
    const manaLine = d3.line()
        .x(d => x(d.key))
        .y(d => yRight(d.value))
        .curve(d3.curveMonotoneX);

    svg.append("path")
        .datum(manaDataArray)
        .attr("fill", "none")
        .attr("stroke", "var(--mana)")
        .attr("stroke-width", 1.5)
        .attr("d", manaLine);

    const legendData = [
        { label: "Healing", color: "var(--healing-font)" },
        { label: "Mana", color: "var(--mana)" }
    ];

    const legend = svg.selectAll(".legend")
        .data(legendData)
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", (d, i) => "translate(0," + i * 20 + ")");

    legend.append("rect")
        .attr("x", width - 38)
        .attr("y", -10)
        .attr("width", 35)
        .attr("height", 1)
        .style("fill", d => d.color);

    legend.append("text")
        .attr("x", width - 44)
        .attr("y", -10)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(d => d.label)
        .style("fill", "white")
        .style("font-size", "12px");

    return svg;
};

export { createHealingLineGraph };