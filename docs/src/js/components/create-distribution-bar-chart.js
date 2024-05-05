import { formatNumbers } from './index.js';

const createBellCurveBarChart = (data, graphId, title, colour) => {
    const values = Object.values(data);

    const minValue = Math.min(...values);
    const maxValue = Math.max(...values) + 100;

    const numIntervals = 50;
    const range = maxValue - minValue;
    const intervalWidth = range / numIntervals;
    const intervalCounts = Array(numIntervals).fill(0);

    values.forEach(value => {
        const intervalIndex = Math.floor((value - minValue) / intervalWidth);
        intervalCounts[intervalIndex]++;
    });

    const intervals = Array.from({ length: numIntervals }, (_, i) => {
        const intervalMin = minValue + i * intervalWidth;
        const intervalMax = i === numIntervals ? maxValue + 1 : intervalMin + intervalWidth;

        return { interval: `${formatNumbers(intervalMin)} - ${formatNumbers(intervalMax)}`, count: intervalCounts[i] };
    });

    const percentileBrackets = intervals.map(interval => {
        const intervalMin = parseFloat(interval.interval.split(" - ")[0].replace(/,/g, ''));
        const intervalMax = parseFloat(interval.interval.split(" - ")[1].replace(/,/g, ''));
    
        const percentile25 = d3.quantile(values.sort((a, b) => a - b), 0.25);
        const percentile50 = d3.quantile(values.sort((a, b) => a - b), 0.53);
        const percentile75 = d3.quantile(values.sort((a, b) => a - b), 0.75);
        const percentile95 = d3.quantile(values.sort((a, b) => a - b), 0.95);
        const percentile98 = d3.quantile(values.sort((a, b) => a - b), 0.989);
        const percentile99 = d3.quantile(values.sort((a, b) => a - b), 0.999);
    
        let intervalPercentile;
        if (intervalMax <= percentile25) {
            intervalPercentile = 25;
        } else if (intervalMax <= percentile50) {
            intervalPercentile = 50;
        } else if (intervalMax <= percentile75) {
            intervalPercentile = 75;
        } else if (intervalMax <= percentile95) {
            intervalPercentile = 95;
        } else if (intervalMax <= percentile98) {
            intervalPercentile = 98.9;
        } else if (intervalMax <= percentile99) {
            intervalPercentile = 99.9;
        } else {
            intervalPercentile = 100;
        };
    
        return {
            interval: interval.interval,
            percentile: intervalPercentile
        };
    });

    const margin = { top: 30, right: 30, bottom: 75, left: title === "HPS" ? 75 : 45 },
        width = 1240 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    const svgContainer = d3.select(graphId).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("background", "transparent");

    const svg = svgContainer.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand()
        .domain(intervals.map(d => d.interval))
        .range([0, width])
        .padding(0.1);

    const y = d3.scaleLinear()
        .domain([0, d3.max(intervals, d => d.count)])
        .range([height, 0]);

        svg.selectAll(".bar")
            .data(intervals)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", d => x(d.interval))
            .attr("y", d => y(d.count))
            .attr("width", x.bandwidth())
            .attr("height", d => height - y(d.count))
            .attr("fill", d => {
                const percentileBracket = percentileBrackets.find(pb => pb.interval === d.interval);
                if (percentileBracket) {
                    const percentile = percentileBracket.percentile;
                    if (percentile <= 25) return "#666";
                    if (percentile <= 50) return "#1eff00";
                    if (percentile <= 75) return "#0070ff";
                    if (percentile <= 95) return "#a335ee";
                    if (percentile <= 98.9) return "#ff8000";
                    if (percentile <= 99.9) return "#e268a8";
                }
                return "#e5cc80";
            });

    const xAxisGroup = svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x).tickFormat(() => "").tickSize(0));

    xAxisGroup.append("text")
        .attr("class", "axis-label")
        .attr("x", (width / 2) - 10)
        .attr("y", 45)
        .style("text-anchor", "middle")
        .text("HPS");

    xAxisGroup.append("text")
        .attr("class", "axis-label")
        .attr("x", -17)
        .attr("y", 35)
        .style("text-anchor", "start")
        .text(`${formatNumbers(minValue)}`);
    
    xAxisGroup.append("text")
        .attr("class", "axis-label")
        .attr("x", width + 17)
        .attr("y", 35)
        .style("text-anchor", "end")
        .text(`${formatNumbers(maxValue)}`);

    xAxisGroup.selectAll("text").style("fill", "white");

    const maxTicks = 15;

    const yAxisGroup = svg.append("g")
        .call(d3.axisLeft(y)
        .ticks(Math.min(maxTicks, d3.max(intervals, d => d.count) + 1))
        .tickFormat(d => Math.round(d)));

    yAxisGroup.append("text")
        .attr("class", "axis-label")
        .attr("transform", "rotate(-90)")
        .attr("x", -height / 2)
        .attr("y", title === "HPS" ? -55 : -30)
        .style("text-anchor", "middle")
        .text("Iterations");

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
            const index = Math.floor((adjustedMouseX / width) * intervals.length);
            const interval = intervals[index].interval;
            const count = intervals[index].count;

            tooltip.html(`<span class="tooltip-time">${interval}</span><br/>`)
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

    return svg;
};

const createLowestToHighestBarChart = (data, graphId, title, colour) => {
    const dataArray = Object.keys(data)
        .map(key => ({ key: +key, value: data[key] }))
        .sort((a, b) => a.value - b.value);
    
    const margin = { top: 30, right: 30, bottom: 75, left: title === "HPS" ? 75 : 45 },
        width = 1240 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;
        
    const svgContainer = d3.select(graphId).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("background", "transparent");

    const svg = svgContainer.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand()
        .domain(dataArray.map(d => d.key))
        .range([0, width])
        .padding(0.1);
        
    const y = d3.scaleLinear()
        .domain([0, d3.max(dataArray, d => d.value)])
        .range([height, 0]);

    svg.selectAll(".bar")
        .data(dataArray)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", d => x(d.key))
        .attr("y", d => y(d.value))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d.value))
        .attr("fill", colour);

    const xAxisGroup = svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x).tickFormat(() => "").tickSize(0));

    xAxisGroup.append("text")
        .attr("class", "axis-label")
        .attr("x", (width / 2) - 10)
        .attr("y", 51)
        .style("text-anchor", "middle")
        .text("Iterations");

    xAxisGroup.selectAll("text").style("fill", "white");

    const yAxisGroup = svg.append("g")
        .call(d3.axisLeft(y).ticks().tickFormat(d3.format(".2s")));

    yAxisGroup.append("text")
        .attr("class", "axis-label")
        .attr("transform", "rotate(-90)")
        .attr("x", -height / 2)
        .attr("y", title === "HPS" ? -60 : -30)
        .style("text-anchor", "middle")
        .text(title);

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
            const index = Math.floor((adjustedMouseX / width) * dataArray.length);
            const iteration = dataArray[index].key;
            const hps = dataArray[index].value;

            tooltip.html(`<span id="tooltip-${title.toLowerCase().replaceAll(" ", "-")}">${title === "HPS" ? formatNumbers(hps) : Math.round(hps * 10) / 10}</span>`)
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

export { createBellCurveBarChart, createLowestToHighestBarChart };
