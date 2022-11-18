// The basic chart options
const chartOptions = {
    width: 550,
    type: 'pie',
};

// Make the pie chart responsive
const responsiveOptions = [{
    breakpoint: 5500,
    options: {
        chart: {
            width: 450
        },
        legend: {
            position: 'bottom'
        },
        dataLabels: {
            enabled: true,
            style: {
                fontSize: "12px",
            }
        }
    }
},
{
    breakpoint: 450,
    options: {
        chart: {
            width: 350
        },
        legend: {
            position: 'bottom'
        },
        dataLabels: {
            enabled: true,
            style: {
                fontSize: "12px",
            }
        }
    }
},
{
    breakpoint: 350,
    options: {
        chart: {
            width: 300
        },
        legend: {
            position: 'bottom'
        },
        dataLabels: {
            enabled: true,
            style: {
                fontSize: "11px",
            }
        }
    }
},
{
    breakpoint: 300,
    options: {
        chart: {
            width: 275
        },
        legend: {
            position: 'bottom'
        },
        dataLabels: {
            enabled: true,
            style: {
                fontSize: "10px",
            }
        }
    }
}
];

// The chart options
var options = {
    series: [], // the data
    chart: chartOptions, // the chart options
    labels: electionCategories, // categories/labels (yes/no or candidate names (depending on the election type))
    legend: {
        position: 'bottom',
        fontSize: '12px',
    },
    responsive: responsiveOptions // the responsive options
};
var myChartDiv, electionTotalVotes;

// returns the chart options
const getChartOptions = (chosenOption) => {
    options.series = electionFilters[chosenOption]; // the filter of the votes being chosen for display (e.g. adjusted votes, kisa votes etc.)
    if(chosenOption == 'Adjusted Votes') { // if the adjusted votes are being displayed
        // do not have tooltip when hovered over the chart (since it won't mean anything)
        options['tooltip'] = {
            y: {
                formatter: function(value, { series, seriesIndex, dataPointIndex, w }) {
                    return undefined
                }
            }
        }
        // accumulate all the votes for showing the total number of votes on the right top corner
        all_votes = 0;
        all_votes += electionFilters['KISA Votes'].reduce((a, b) => a + b, 0);
        all_votes += electionFilters['Non-KISA Votes'].reduce((a, b) => a + b, 0);
        $(electionTotalVotes).text(all_votes);
    }
    else {
        // have tooltip when hovered over the chart, showing the number of votes associated with the category
        options['tooltip'] = {
            y: {
                formatter: function(value, { series, seriesIndex, dataPointIndex, w }) {
                    return value
                }
            }
        }
        $(electionTotalVotes).text(options.series.reduce((a, b) => a + b, 0));
    }
    // assign the explanation of the chosen filter to the explanation div (question mark)
    $('#election-question-mark').attr('data-original-title', electionExplanations[chosenOption]);
    return options;
}

// When the chosen filter is changed/updated
$('.election-dropdown-option').click((e) => {
    const chosenOption = e.target.innerText;
    $('#election-dropdown-button').text(chosenOption);
    $(myChartDiv).empty()
    chart = new ApexCharts(myChartDiv, getChartOptions(chosenOption));
    chart.render();
});

// When the page is loaded
$(document).ready(() => {
    $('#election-question-mark').tooltip(); // adds a tooltip to the question mark button 
    // (the tooltip shows the explanation associated with the chosen filter)
    dropdownOptions = $('.election-dropdown-option'); // the list of filters
    // assign styles to the filter buttons in the dropdown
    dropdownOptions.each(function() {
        $(this).hover(function() {
            $(this).css('background-color', '#FAFAFA');
        }, function() {
            $(this).css('background-color', 'white');
        })
    });
    // get the div element supposed to render the pie chart
    myChartDiv = $("#myChart")[0];
    // get the div element supposed to show the total votes (on the right top corner)
    electionTotalVotes = $('#election-total-votes')[0];
    // create a new pie chart with the chart options for the default filter: adjusted votes
    chart = new ApexCharts(myChartDiv, getChartOptions('Adjusted Votes'));
    // render the chart
    chart.render();
});

