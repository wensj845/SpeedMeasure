/*
 Author: wensujian, huangkai
 create: 2022年11月12日 11:12:23
*/


function authority(){
    $.ajax({
        url: '/auth/',
        type: 'GET',
        dataType: 'json',
        async: false,
        success: function (data) {
            if (data.code == "200") {
                  if (data.admin == 0){
                    if (document.getElementById("adNav") != null){
                        document.getElementById("adNav").style.display = "none";
                    }
                    if (document.getElementById("baseline_btn") != null){
                        document.getElementById("baseline_btn").style.display = "none";
                    }
                    console.log("^^^^^^^^^^^^^^^^^^^")
                    console.log(document.getElementsByName("delb").length)
                    for(let i=0;i<document.getElementsByName("delb").length;i++){
                        document.getElementsByName("delb")[i].style.display = "none";
                    }
                  }
                  console.log("data.name=",data.name)
                  document.getElementById("logOut").innerHTML = '<a><span class="glyphicon glyphicon-user"></span>'+"  " +data.name +'</a><a href="/auth/logout"><span class="glyphicon glyphicon-log-in"></span>  退出登录</a>'
            }
        }
    });
}

function register(){
    console.log("$$$$$$$$$$$$$$$$$$$$$")
    console.log("注册")
}