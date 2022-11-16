function newProject(){
    var project = document.getElementById("addProject").value
    var result = ""
    var projects = []
    console.log(project)
    //判断新建的工程是否为空
    if(isNull(project)){
        alert("项目内容不能为空!")
        return
    }

    $.ajax({
        data: {"project": project},
        url: '/setting/project',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            if (data.code == "200") {
                projects = data.projects
                for(var i = 0;i < projects.length;i++){
                    result = result + "<option>"+ projects[i] +"</option>"
                }
            } else {
                    alert("addProject() error");
                }
            alert("添加项目成功！")
            document.getElementById("selectProject").innerHTML = result
        }
    });
    window.location.reload()
}

function newFunction(){
    var project = document.getElementById("selectProject").value
    var functionTxt = document.getElementById("function_txt").value
    var result = ""
    var projects = []
    console.log(project)
    console.log(functionTxt)

    //判断新建的功能点是否为空
    if(isNull(functionTxt)){
        alert("功能点内容不能为空!")
        return
    }

    $.ajax({
        data: {"project": project,"function":functionTxt},
        url: '/setting/function',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            if (data.code == "200") {
                alert("添加功能点成功！")
            }
        }
    });
    window.location.reload()
}

function delFuc(obj){
    var fuc_id = obj.id.split('_')[1]
    console.log(fuc_id);

    $.ajax({
        data: {"fuc_id": fuc_id},
        url: '/setting/delf',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            if (data.code == "200") {
                alert("删除功能点成功！")
            }
        }
    });
    window.location.reload()
}

function delPro(obj){
    var pro_id = obj.id.split('_')[1]
    console.log(pro_id);

    $.ajax({
        data: {"pro_id": pro_id},
        url: '/setting/delp',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            if (data.code == "200") {
                alert("删除项目成功！")
            }
        }
    });
    window.location.reload()
}

function getProjectsAndFunctions(){
    var result = ""
    var projects = []
    var functions = []
    var function_ids = []
    $.ajax({
        url: '/setting/getProjectsAndFunctions',
        type: 'GET',
        success: function (data) {
            console.log(data)
            projects = data.projects
            functions = data.functions
            function_ids = data.function_ids
            if (data.code == "200") {
                //功能点清单
                for(var i = 0;i < projects.length;i++){
                    result = result + "<tr class='mtd'><td>"+projects[i]+"</td>"
                    result = result + "<td>"+functions[i]+"</td>"
                    result = result + '<td><button type="button" id="'+"fuc_"+function_ids[i]+'" onclick="delFuc(this)" class="btn btn-sm btn-danger">删除</button></td></tr>'
                }
                document.getElementById("function_all").innerHTML = result
//                btn btn-danger dbtn
            }
        }
    });
}

function getProjects(){
    var result = ""
    var projects = []
    var project_ids = []
    $.ajax({
        url: '/setting/getPro',
        type: 'GET',
        success: function (data) {
            console.log(data)
            projects = data.projects
            project_ids = data.project_ids
            if (data.code == "200") {
                //项目清单
                for(var i = 0;i < projects.length;i++){
                    result = result + "<tr class='mtd'><td>"+projects[i]+"</td>"
                    result = result + '<td><button type="button" id="'+"pro_"+project_ids[i]+'" onclick="delPro(this)" class="btn btn-sm btn-danger">删除</button></td></tr>'
                }
                document.getElementById("project_all").innerHTML = result
            }
        }
    });
}

function isNull(str){
    if ( str == "" ) return true;
    var regu = "^[ ]+$";
    var re = new RegExp(regu);
    return re.test(str);
}

$(document).ready(function(){
  $("input").focus(function(){
    $(this).css("background-color","#cccccc");
  });
  $("input").blur(function(){
    $(this).css("background-color","#ffffff");
  });
  $("button").click(function(){
    $(this).animate({opacity:'0.6'});
    $(this).animate({opacity:'1'});
  });
});