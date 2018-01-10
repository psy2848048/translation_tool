var pageScript = function(){
    var local = this;
    this.preInits = function(){
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
    this.selectEvent = function(){
        $('#file_upload_frm').on('change', function(e){
            e.preventDefault();
            //var reg_ext = ['JPG','JPEG','GIF','PNG'];
            var reg_ext = ['CVS'];
            var msg = 'cvs 파일 확장자만 허용합니다.';
            onFileSelect($('#file_upload_frm'), '파일을받을서버URL', 15, reg_ext, msg);
        });        
    };
    this.showPopup = function () {
        $('#mainWrap').css('opacity', '0.2');
        $("#upload_div").show();
        $("#upload_div").center();
    };
    this.bind = function(){
        local.preInits();
        local.keyupEvents();
        local.clickEvents();
        local.selectEvent();
    };
};
$(function(){
    var script = new pageScript();
    script.bind();
});




