$( document ).ready(function (){
    $(".sidenav").append('<h1>Menu</h1> '+
        '<h3>Manage</h3> ' +
        '<form method="POST" action="things">'+
        '    <button type="submit"><i class="fa fa-archive" aria-hidden="true"></i> Things</button>'+
        '</form>'+
        '<form method="POST" action="users">'+
        '    <button type="submit"><i class="fa fa-user" aria-hidden="true"></i> Users</button>'+
        '</form>'+
        '<form method="POST" action="locations">'+
        '    <button type="submit"><i class="fa fa-map-marker" aria-hidden="true"></i> Locations</button>'+
        '</form>'+
        '<h3>About</h3>'+
        '<form method="POST" action="about">'+
        '    <button type="submit"><i class="fa fa-info" aria-hidden="true"></i> About us</button>'+
        '</form>'+
        '<h3>Exit</h3>'+
        '<form method="POST" action="quit">'+
        '    <button type="submit"><i class="fa fa-sign-out" aria-hidden="true"></i> Logout</button>'+
        '</form>')
})