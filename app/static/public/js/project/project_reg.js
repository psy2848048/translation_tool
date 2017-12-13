var PageScript = function(){
    var local = this,
        project_id = getUrlParameter('project');
	this.preInits = function(){  
    };
	this.btnEvents = function(){ 
    };
    this.bind = function(){
        local.preInits();
        local.btnEvents();
    };
};
$(function(){
    var script = new PageScript();
    script.bind();
    alert(script.project_id);
});