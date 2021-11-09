var image_update_timer = null;
var active_station = null;
var active_nav = null;

function construct_ui()
{
  console.info("Creating UI")
  fetch("/rest/Stations")
    .then((resp) => {return resp.json()})
    .then((stations) => {
      let station_list = document.getElementById('station_list');
      let count = 0;
      for (let station of stations)
      {
        console.info(JSON.stringify(station));
        let nav_item = document.createElement("div");
        nav_item.className = "nav-item";
        station_list.appendChild(nav_item);
        let html_content = `<b>${station.name}</b> <br />
        Last Image Update: <i>${station.last_image}</i>`;
        if (station.space_available && station.space_available > 0)
        {
          let free_space = Math.round(station.space_available);
          html_content += `<br/>Free space: ${free_space}%`;
        }
        else if (station.space_available && station.space_available==-1)
        {
          html_content += `<br/>System is not recording`;
        }
        nav_item.innerHTML = html_content;
        nav_item.addEventListener("click", (evt) => {
          set_active_station(nav_item, station)
        });
        if (count == 0)
        {
          set_active_station(nav_item, station);
        }
        count++;
      }

      let nav_item = document.createElement("div");
      nav_item.className = "nav-item";
      station_list.append(nav_item);
      nav_item.textContent = "Logout";
      nav_item.addEventListener("click", () => {
        window.location.href="/accounts/logout/"
      });
    });

}

function set_active_station(nav_item, station_info)
{
  if (image_update_timer)
  {
    clearTimeout(image_update_timer);
  }
  if (active_nav)
  {
    active_nav.classList.remove("nav-item-selected");
  }
  active_station = station_info;
  active_nav = nav_item;
  active_nav.classList.add("nav-item-selected");
  update_display();
}

function update_display()
{
  if (active_station == null)
  {
    console.warn("Can't update, no station known");
    return;
  }
  let station_image = document.getElementById("station_image");
  let station_name = document.getElementById("station_name");
  station_name.textContent = active_station.name;
  station_image.src = active_station.image + "?" + new Date().getTime();
  image_update_timer = setTimeout(update_display, 30000);
}

window.onload = construct_ui();
