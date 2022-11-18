const chartOptions = {
    width: 550,
    type: 'pie',
};

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

var options = {
    series: [],
    chart: chartOptions,
    labels: electionCategories,
    legend: {
        position: 'bottom',
        fontSize: '12px',
    },
    responsive: responsiveOptions
};
var myChartDiv, electionTotalVotes;

const getChartOptions = (chosenOption) => {
    options.series = electionFilters[chosenOption];
    if(chosenOption == 'Adjusted Votes') {
        options['tooltip'] = {
            y: {
                formatter: function(value, { series, seriesIndex, dataPointIndex, w }) {
                    return undefined
                }
            }
        }
        all_votes = 0;
        all_votes += electionFilters['KISA Votes'].reduce((a, b) => a + b, 0);
        all_votes += electionFilters['Non-KISA Votes'].reduce((a, b) => a + b, 0);
        $(electionTotalVotes).text(all_votes);
    }
    else {
        options['tooltip'] = {
            y: {
                formatter: function(value, { series, seriesIndex, dataPointIndex, w }) {
                    return value
                }
            }
        }
        $(electionTotalVotes).text(options.series.reduce((a, b) => a + b, 0));
    }
    $('#election-question-mark').attr('data-original-title', electionExplanations[chosenOption]);
    return options;
}

$('.election-dropdown-option').click((e) => {
    const chosenOption = e.target.innerText;
    $('#election-dropdown-button').text(chosenOption);
    $(myChartDiv).empty()
    chart = new ApexCharts(myChartDiv, getChartOptions(chosenOption));
    chart.render();
});

$(document).ready(() => {
    $('#election-question-mark').tooltip();
    dropdownOptions = $('.election-dropdown-option');
    dropdownOptions.each(function() {
        $(this).hover(function() {
            $(this).css('background-color', '#FAFAFA');
        }, function() {
            $(this).css('background-color', 'white');
        })
    });
    myChartDiv = $("#myChart")[0];
    electionTotalVotes = $('#election-total-votes')[0];
    chart = new ApexCharts(myChartDiv, getChartOptions('Adjusted Votes'));
    chart.render();
});

