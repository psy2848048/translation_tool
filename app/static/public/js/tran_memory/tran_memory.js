var pageScript = function(){
    var local = this;
    this.preInits = function(){
        jQuery.fn.center = function () {
            this.css("position", "absolute");
            this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2 - 100) + $(window).scrollTop()) +
                "px");
            this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) + $(window).scrollLeft()) +
                "px");
            return this;
        };
    };
    this.showPopup = function () {
        $('#mainWrap').css('opacity', '0.2');
        $("#upload_div").show();
        $("#upload_div").center();
    };
    this.keyupEvents = function(){
        $(document).on('keyup', '#listTitleGroup textarea', function (e){
            e.preventDefault();            
            $(this).css('height', 'auto' );
            $(this).height( this.scrollHeight );
        });
        $('#listTitleGroup').find('textarea').keyup();
    };
    this.clickEvents = function(){
        $('#new_li_btn').on('click', function(e){
            e.preventDefault();
            local.showPopup();
        });
        $('#listTitleGroup table td .fa-times').on('click', function(e){
            e.preventDefault();
            alert('현재 줄 삭제');
        });
        $('#upload_div .fa-times').on('click', function(e){
            e.preventDefault();
            $('#upload_div').hide();
            $('#mainWrap').css('opacity', '1');
        });
    };
    this.bind = function(){
        local.preInits();
        local.keyupEvents();
        local.clickEvents();
    };
};
$(function(){
    var script = new pageScript();
    script.bind();
});