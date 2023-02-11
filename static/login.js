xfunction eyeclicklg(){
    let itpwd = document.getElementById('inputPassword')
    let eye = document.getElementById('eyes');
    let open = "btn btn-default glyphicon glyphicon-eye-open"
    let close = "btn btn-default glyphicon glyphicon-eye-close"
    if(eye.className == open){
      eye.className = close;
      itpwd.type = "password"
    }else{
      eye.className = open;
      itpwd.type = "text"
    }
}

function eyeclick(){
    let itpwd = document.getElementById('rPwd')
    let eye = document.getElementById('eyes');
    let open = "btn btn-default glyphicon glyphicon-eye-open"
    let close = "btn btn-default glyphicon glyphicon-eye-close"
    if(eye.className == open){
      eye.className = close;
      itpwd.type = "password"
    }else{
      eye.className = open;
      itpwd.type = "text"
    }
  }
function eyeclick2(){
    let itpwd = document.getElementById('raPwd')
    let eye = document.getElementById('eyes2');
    let open = "btn btn-default glyphicon glyphicon-eye-open"
    let close = "btn btn-default glyphicon glyphicon-eye-close"
    if(eye.className == open){
      eye.className = close;
      itpwd.type = "password"
    }else{
      eye.className = open;
      itpwd.type = "text"
    }
  }