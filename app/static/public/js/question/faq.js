var pageScript = function(){
    var local = this;
    this.clickEvent = function(){
        $('#faqSection div h4').on('click', function(e){
            e.preventDefault();   
            $(this).next().slideToggle();
        });
    },
    this.bind = function(){
        local.clickEvent();
    };
}
$(function(){
    var script = new pageScript();
    script.bind();
});