// console.log('Write your JS code here!');
$('.faq-heading').click(function () {

    $(this).parent('li').toggleClass('the-active').find('.faq-text').slideToggle();
});
$('.cat-heading').click(function () {

    $(this).parent('li').toggleClass('the-active').find('.cat-text').slideToggle();
});
