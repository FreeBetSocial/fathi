const url = "https://ff.xox.su/api/"

export const get =()=>fetch(url+"get",{method:"POST"}).then(e=>e.json())
export const update = (items)=>fetch(url+"update",{method:"POST", headers:{"content-type":"application/json"}, body:JSON.stringify({title:"",items})}).then(e=>e.json())
export const mathGrapg = (_from,_to,_block=[])=>fetch(url+`math_graph?_from=${_from}&_to=${_to}`,{method:"POST", headers:{"content-type":"application/json"}, body:JSON.stringify(_block)}).then(e=>e.json())