for (let toy of document.querySelectorAll('.toy')){
    toy.onclick = () => {
        buy_combobox(toy);
    }
}

document.getElementById("close_x").onclick = () => {
    document.getElementById("buy_toys").style.visibility = "hidden";
}

function buy_combobox(toy){
    buy_toys = document.getElementById("buy_toys")
    buy_toys.style.visibility = "visible";

    for (let buy_var of document.querySelectorAll('.toy_var')) {
        buy_var.onclick = () => {
            toy_slot_id = toy.id.charAt(4);
            toy_type_id = buy_var.getElementsByClassName('toy_img')[0].src.charAt(buy_var.getElementsByClassName('toy_img')[0].src.length - 5);
            user_id = parseInt(document.getElementById('info').innerHTML);

            $.post(`http://127.0.0.1:8080/api/v1/buy_toy/?user_id=${user_id}&slot=${toy_slot_id}&toy=${toy_type_id}`, {user_id: {user_id}, slot: {toy_slot_id}, toy_id: {toy_type_id}},
                function(data){
                    parse_data = JSON.parse(data);
                    buy_toys.style.visibility = "hidden";
                    alert(parse_data.message);
                    if (parse_data.success){
                        document.getElementById("exp").innerHTML = "🎉" + parse_data.exp;
                        set_toys();
                        return;

                    }
                })
            }
        }
    }


function set_toys(){
    let user_id = parseInt(document.getElementById('info').innerHTML);

    $.ajax({
        url: "http://127.0.0.1:8080/api/v1/get_user_toys/?user_id=" + user_id,
        success: function (data) {
            let items = JSON.parse(data).items;
            console.log(items);

            for (let item of items){
                toy_slot = document.getElementById("toy_" + item[3]).getElementsByClassName('toy-item')[0];
                toy_slot.innerHTML = '';
                toy_slot_img = document.createElement("img");
                toy_slot_img.className = "toy_slot_img";
                toy_slot_img.src = toys.get("toy_" + item[2]);
                console.log(toys.get("toy_1"));
                toy_slot.append(toy_slot_img);
            }
        }

        })
}

set_toys();