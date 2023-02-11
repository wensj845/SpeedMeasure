//速度测量
var measure_time = 0
var measure_time_s = 0

function updateSelectFunction(selectedValue){
    $.ajax({
        url: '/speedmeasure/getFunctionByProjId',
        type: 'GET',
        data: { Value: selectedValue},
        dataType: "json",
        success: function (data) {
            console.log(data)
            if (data.code == "200") {
                //项目清单
                functions = data.functions
                functions = data.functions
                for(var i = 0;i < functions.length;i++){
                    $("#save_sel_function").append($('<option value=' + functions[i][1] + '>' + functions[i][0] + '</option>'));
                    $("#smart_sel_function").append($('<option value=' + functions[i][1] + '>' + functions[i][0] + '</option>'));
                    $("#base_sel_function").append($('<option value=' + functions[i][1] + '>' + functions[i][0] + '</option>'));
                }
                $("#save_sel_function").trigger("click")
                $("#smart_sel_function").trigger("click")
                $("#base_sel_function").trigger("click")
            }
        }
    });
}

function getAllProjects(){
    $.ajax({
        url: '/speedmeasure/getProject',
        type: 'GET',
        success: function (data) {
            console.log(data)
            if (data.code == "200") {
                //项目清单
                projects = data.projects
                init_project_id = projects[0][1]
                for(var i = 0;i < projects.length;i++){
                    $("#save_sel_project").append($('<option value=' + projects[i][1] + '>' + projects[i][0] + '</option>'));
                    $("#smart_sel_project").append($('<option value=' + projects[i][1] + '>' + projects[i][0] + '</option>'));
                    $("#base_sel_project").append($('<option value=' + projects[i][1] + '>' + projects[i][0] + '</option>'));
                }

                //$("#save_sel_project").trigger("click")
            }
        }
    });
}

function saveResult() {
    var save_project_select = $("#save_sel_project option:selected");　　　　//获取选中项
    var save_function_select = $("#save_sel_function option:selected");　　　　//获取选中项
    var project_id = save_project_select.val();　　　　　　　　　　　　　　//获取选中项的值
    var function_id = save_function_select.val();　
    console.log("project_id",project_id)
    console.log("function_id",function_id)
    var duration = measure_time
    var timestamp = new Date().getTime();
    $.ajax({
        data: {"project_id": project_id, "function_id": function_id,"duration":duration,"timestamp":timestamp},
        url: '/speedmeasure/save',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            if (data.code == "200") {
                document.getElementById("show_start_time").innerHTML = "本次耗时为 " + measure_time_s.toString()+ " 毫秒，数据保存成功！"
                //alert("测试结果存档成功");
            } else {
                document.getElementById("show_start_time").innerHTML = "测试结果存档失败，请检查项目和功能点是否存在！"
                //alert("测试结果存档失败，请检查项目和功能点是否存在！");
            }
        }
    });
}

function speedMeasure() {
    var inputElements = document.getElementsByTagName("input")
    var count = 0
    var startFrame = -1
    var endFrame = -1
    for (var i = 0; i < inputElements.length; i++) {
        if (inputElements[i].type === "checkbox" && inputElements[i].checked === true) {
            if (startFrame == -1) {
                startFrame = inputElements[i].value
            } else {
                endFrame = inputElements[i].value
            }
            count++
        }
    }
    if (count < 2) {
        alert("请选择两帧图片")
        return
    }
    console.log(startFrame)
    console.log(endFrame)
    $.ajax({
        data: {"startFrame": startFrame, "endFrame": endFrame},
        url: '/speedmeasure/measure',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            if (data.code == "200") {
                measure_time = data.result
                document.getElementById("save_btn").removeAttribute("disabled");
            } else {
                alert("度量计算失败，请重新计算");
            }
            //耗时折算成秒
            //measure_time_s = measure_time/1000
            measure_time_s = measure_time
            document.getElementById("show_start_time").innerHTML = "<b>本次耗时为 " + measure_time_s.toString()+ " 毫秒</b>"
        }
    });
}

//智能选帧逻辑
function smartFrameSel(){
    var smart_function_select = $("#smart_sel_function option:selected");
    var function_id = smart_function_select.val();　　　　　　　　　　　　　　//获取选中项的值
    var startFrame
    var endFrame
    try{
        var imagePath = document.getElementById("qushuju").getAttribute('value').split('-')[0]
        var imageNum = parseInt(document.getElementById("qushuju").getAttribute('value').split('-')[1])
    }catch(error){
        var imagePath = sessionStorage.getItem("imgfile").split('-')[0]
        var imageNum = parseInt(sessionStorage.getItem("imgfile").split('-')[1])
    }
    console.log("function_id",function_id)
    console.log("imagePath",imagePath)
    console.log("imageNum",imageNum)
    //智能选帧按钮置灰，等后台处理完
    document.getElementById("smart_btn").setAttribute("disabled",true);
    document.getElementById("smart_confirm").setAttribute("disabled",true);
//    document.getElementById("smart_prompt").innerHTML = "开始智能选帧，请稍后..."
    //开启智能选帧进度条
    setSmartProgress();

    $.ajaxSettings.async = true;
    $.ajax({
        data: {"function_id": function_id,"imagePath": imagePath,"imageNum": imageNum},
        url: '/speedmeasure/smartSelect',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data.startFrame)
            console.log(data.endFrame)
            if (data.code == "200") {
                var inputElements = document.getElementsByTagName("input")
                //先重置选帧，接着将指定的帧选中
                for (var i = 0; i < inputElements.length; i++) {
                    if (inputElements[i].type == "checkbox" && inputElements[i].checked == true) {
                        inputElements[i].checked = false
                    }
                    if (inputElements[i].value == data.startFrame || inputElements[i].value == data.endFrame){
                        inputElements[i].checked = true
                    }
                }
//                $("#measure_btn").trigger("click")
                clearSmartProgress()
                document.getElementById("show_start_time").innerHTML = '智能选帧成功，请点击"计算"按钮！'
                document.getElementById("clean_btn").removeAttribute("disabled");
            } else {
                clearSmartProgress()
                document.getElementById("show_start_time").innerHTML = "智能选帧失败，请检查基线数据以及项目和功能点是否存在！"
            }
            document.getElementById("smart_confirm").removeAttribute("disabled");
            document.getElementById("smart_btn").removeAttribute("disabled");
            document.getElementById("smart_prompt").innerHTML = ""
        }
    });
}

var smart_int = 0;
var smart_progress = 10;
function setSmartProgress() {
    smart_progress = 10;
    smart_int = self.setInterval("smart_interval()",1500);
    document.getElementById("smart_progress_bar").style.width = "10%";
    document.getElementById("smart_progress").style.display="";
    document.getElementById("smart_progress_head").style.display = ""
}

function clearSmartProgress(){
    //智能选帧结束后，清除进度条
    smart_int=window.clearInterval(smart_int)
    document.getElementById("smart_progress_bar").style.width = "100%";
    setTimeout("hideSmartProgress()", 300)
}

function hideSmartProgress(){
    document.getElementById("smart_progress").style.display="none";
    $("#smart_cancel").trigger("click")
}

function smart_interval(){
    if(smart_progress < 100){
        smart_progress = smart_progress + 10
    }
    document.getElementById("smart_progress_bar").style.width = smart_progress.toString() + "%";
}


function saveBase(){
    var base_function_select = $("#base_sel_function option:selected");
    var function_id = base_function_select.val();　　　　　　　　　　　　　　//获取选中项的值
    var inputElements = document.getElementsByTagName("input")
    var count = 0
    var startFrame = -1
    var endFrame = -1
    try{
        var imagePath = document.getElementById("qushuju").getAttribute('value').split('-')[0]
    }catch(error){
        var imagePath = sessionStorage.getItem("imgfile").split('-')[0]
    }
    console.log("function_id",function_id)
    //保存基线按钮置灰，等后台处理完
    document.getElementById("baseline_btn").setAttribute("disabled",true);

    for (var i = 0; i < inputElements.length; i++) {
        if (inputElements[i].type === "checkbox" && inputElements[i].checked === true) {
            if (startFrame == -1) {
                startFrame = inputElements[i].value
            } else {
                endFrame = inputElements[i].value
            }
            count++
        }
    }
    if (count < 2) {
        document.getElementById("show_start_time").innerHTML = '保存基线失败，请至少选择两帧图片！'
        document.getElementById("baseline_btn").removeAttribute("disabled");
        return
    }
    console.log(startFrame)
    console.log(endFrame)
    $.ajax({
        data: {"function_id": function_id,"startFrame": startFrame, "endFrame": endFrame,"imagePath": imagePath,},
        url: '/speedmeasure/base',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            if (data.code == "200") {
                document.getElementById("show_start_time").innerHTML = '保存基线成功！'
            } else {
                document.getElementById("show_start_time").innerHTML = '保存基线失败，请检查项目和功能点是否存在！'
            }
            document.getElementById("baseline_btn").removeAttribute("disabled");
        }
    });

}

$(document).ready(function(){
  $("input").click(function(){
    $(this).animate({opacity:'0.6'});
    $(this).animate({opacity:'1'});
  });
  $("#measure_btn").click(function(){
    $(this).animate({opacity:'0.6'});
    $(this).animate({opacity:'1'});
  });
});



