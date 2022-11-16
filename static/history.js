/*
 Author: wensujian, huangkai
 create: 2022年11月6日20:35:23
*/
function changeTimeFormat(time) {
    let date = new Date(time);
    let month = date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date.getMonth() + 1;
    let currentDate = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
    let hh = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
    let mm = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
    return date.getFullYear() + "-" + month + "-" + currentDate+" "+hh + ":" + mm;
}

function delrest(id,fid) {
       console.log("属于哪一个方法呢？")
       console.log(fid)
    $.ajax({
        data: {"rtid": id},
        url: '/history/del',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            if (data.code == "200") {
                  console.log(data)
                  reloadClick(fid)
            }
        }
    });
}


function report(data) {
        const myChart = echarts.init(document.getElementById('ert'));
        let app = data.functions[0][3]
        let fc = data.functions[0][0]
        let dts = []
        let ts  = []
        for(let i=0;i < data.functions.length;i++){
            dts.push(changeTimeFormat(data.functions[i][2]))
            ts.push(data.functions[i][1])
        }
        const option = {
            title: {
              text: app + ' ' + fc
            },
            tooltip: {},
            grid: {
                bottom: '30%'
            },
            legend: {
              data: [fc + '时间']
            },
            xAxis:{
                data:dts,
                boundaryGap: 0,
                axisLabel:{
                    rotate:60
                }
            },
            yAxis:{},
            series:{
                name: fc + '时间',
                type:'line',
                data:ts,
                smooth:true,
                itemStyle:{
                    color: '#00acec'
                },
                areaStyle:{
                    color: '#00acec',
                    opacity: 0.3
                },
                symbolSize:20,
                symbol: 'pin'
            }
        }
        myChart.setOption(option);
}

function searchFunction(){
    let s1 = document.getElementById("selectProject")
    let pro_id = s1.value
    let result = ""
    let trend = ""
    document.getElementById("data_area").style.display = "none";
    $.ajax({
        data: {"pro_id": s1.value},
        url: '/history/functions',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            if (data.code == "200") {
                  console.log(data.functions)
                  if (data.functions.length > 0){
                        result = result + '<a href="#" class="list-group-item disabled list-rt-item">' + '<div style="float: left;margin-left: 5.5%;">执行方法</div><div style="float: left; margin-left: 16%;">耗时（秒）</div><div style="float: left;margin-left: 15.8%;">最近执行时间</div>' + '<div style="float: right;">执行数</div></a>'
                        for(let i=0;i < data.functions.length;i++){
                            let minSecond = parseInt(data.functions[i][5]) / 1000;
                            let maxSecond = parseInt(data.functions[i][6]) / 1000;
                            maxSecond = maxSecond.toFixed(2)
                            minSecond = minSecond.toFixed(2)
                            dt = changeTimeFormat(data.functions[i][2])
                            result = result + '<a href="#" value="'+data.functions[i][3]+'" class="list-group-item list-rt-item" onclick="aclick(this)">' + '<div style="float: left;margin-left: 6%;">'+data.functions[i][1]+'</div><div style="float: left;margin-left: 18%;">'+minSecond+'</div><div style="float: left;margin-left: 18%;">'+dt+'</div><span class="badge">'+data.functions[i][4]+'</span></a>'
                        }
                  }else{
                    result = result + ''
                  }
            }
            document.getElementById("fcList").innerHTML = result
        }
    });
}

function aclick(obj){
    console.log(obj.getAttribute('value'))
    let func_id = obj.getAttribute('value')
    let result = ""
        $.ajax({
        data: {"func_id": func_id},
        url: '/history/results',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            if (data.code == "200") {
                if (data.functions.length > 0){
                        result = result + '<a href="#" class="list-group-item disabled">' + ' 详情</a>'
                        console.log(result)
                        for(let i=0;i < data.functions.length;i++){
                            dt = changeTimeFormat(data.functions[i][2])
                            console.log("****************")
                            console.log(data.functions)
                            result = result + '<a href="#"  value="'+data.functions[i][0]+'" class="list-group-item list-rt-item da" >' + '<div style="float: left;">'+data.functions[i][0]+'</div><div style="float: left; margin-left: 10%;">'+(parseInt(data.functions[i][1])/1000).toFixed(2)+'</div><div style="float: left;margin-left: 10%;">'+dt+'</div>'+ '<div style="float: right"><button name="delb" type="button" class="btn btn-danger btn-sm dbtn" onclick="delrest('+data.functions[i][4]+','+data.functions[i][5]+')">删除</button></div>' +'</a>'
                        }
                        report(data)
                }
            }
            document.getElementById("data_area").style.display = "block";
            document.getElementById("resList").innerHTML = result
            authority()
        }
    });
}

function reloadClick(fid){
    let result = ""
    $.ajax({
        data: {"func_id": fid},
        url: '/history/results',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            if (data.code == "200") {
                if (data.functions.length > 0){
                        result = result + '<a href="#" class="list-group-item disabled">' + ' 详情</a>'
                        console.log(result)
                        for(let i=0;i < data.functions.length;i++){
                            dt = changeTimeFormat(data.functions[i][2])
                            console.log("****************")
                            console.log(data.functions)
                            result = result + '<a href="#"  value="'+data.functions[i][0]+'" class="list-group-item list-rt-item da" >' + '<div style="float: left;">'+data.functions[i][0]+'</div><div style="float: left; margin-left: 10%;">'+(parseInt(data.functions[i][1])/1000).toFixed(2)+'</div><div style="float: left;margin-left: 10%;">'+dt+'</div>'+ '<div style="float: right"><button type="button" class="btn btn-danger btn-sm dbtn" onclick="delrest('+data.functions[i][4]+','+data.functions[i][5]+')">删除</button></div>' +'</a>'
                        }
                        report(data)
                }
            }
            document.getElementById("data_area").style.display = "block";
            document.getElementById("resList").innerHTML = result
        }
    });
}




function defaultPro(){
    $.ajax({
        url: '/history/defaultPro',
        type: 'GET',
        dataType: 'json',
        async: false,
        success: function (data) {
            if (data.code == "200") {
                  document.getElementById('default').setAttribute('value',data.defaultPro[0])
            }
        }
    });
}

function allData(){
    dft = document.getElementById("default")
    $.ajax({
        data:{'project_id': dft.value},
        url: '/history/allData',
        type: 'GET',
        dataType: 'json',
        async: false,
        success: function (data) {
            if (data.code == "200") {
                  console.log(data.allData)
            }
        }
    });
}

function defaultFuncs(){
    dft = document.getElementById("default")
    let result = ""
    let trend = ""
    $.ajax({
        data: {"pro_id": dft.value},
        url: '/history/functions',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            if (data.code == "200") {
                  console.log(data.functions)
                  if (data.functions.length > 0){
                        result = result + '<a href="#" class="list-group-item disabled list-rt-item">' + '<div style="float: left;margin-left: 5.5%;">执行方法</div><div style="float: left; margin-left: 16%;">耗时（秒）</div><div style="float: left;margin-left: 15.8%;">最近执行时间</div>' + '<div style="float: right;">执行数</div></a>'
                        console.log(result)
                        for(let i=0;i < data.functions.length;i++){
                            let minSecond = parseInt(data.functions[i][5]) / 1000;
                            let maxSecond = parseInt(data.functions[i][6]) / 1000;
                            maxSecond = maxSecond.toFixed(2)
                            minSecond = minSecond.toFixed(2)
                            dt = changeTimeFormat(data.functions[i][2]).trim()
                            result = result + '<a href="#" value="'+data.functions[i][3]+'" class="list-group-item list-rt-item" onclick="aclick(this)">' + '<div style="float: left;margin-left: 6%;">'+data.functions[i][1]+'</div><div style="float: left;margin-left: 18%;">'+minSecond+'</div><div style="float: left;margin-left: 18%;">'+dt+'</div><span class="badge">'+data.functions[i][4]+'</span></a>'
                        }
                  }else{
                    result = result + ''
                  }
            }
            ops = document.getElementById("selectProject").options
            for(let i=0;i<ops.length;i++){
                if (ops[i].value == dft.value){
                    console.log(ops[i])
                    ops[i].setAttribute("selected","true")
                }
            }
            document.getElementById("fcList").innerHTML = result
        }
    });
}