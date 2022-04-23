import { useState, useEffect } from "react"
import { get, update, mathGrapg } from "../config"

const Modal =({setOpen, items})=>{
    const [send,setSend] = useState(false)
    const [from,setFrom] = useState("")
    const [to,setTo] = useState("")
    const [block,setBlock] = useState("")
    const [result,setResult] = useState("")
    return (
        <div className="modal" tabIndex="-1" style={{display:"block"}}>
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">Подсчет маршрута</h5>
                        <button onClick={()=>setOpen(false)} type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body">
                        <div className="input-group mb-3">
                            <input type="text" value={from}  onChange={(e)=>{
                                    setFrom(e.target.value.toLocaleUpperCase())
                            }} className="form-control"  placeholder="From" />
                            <span className="input-group-text">{"=>"}</span>
                            <input value={to} onChange={(e)=>{
                                    setTo(e.target.value.toLocaleUpperCase())
                            }}type="text" className="form-control" placeholder="To" />
                            
                        </div>
                        <div>
                        <input type="text" value={block}  onChange={(e)=>{
                                    setBlock(e.target.value.toLocaleUpperCase().replace(/\s{2,}/g, ' '))
                            }} className="form-control"  placeholder="Block List" />
                        </div>
                        {result.length>0&&<p>{result}</p>}

                    
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-secondary" data-bs-dismiss="modal" onClick={()=>setOpen(false)}>Закрыт</button>
                        <button disabled={send} onClick={()=>{
                            if (send)return
                            setSend(true)
                            mathGrapg(from,to,block.split(" ")).then(e=>{
                                setSend(false)
                                setResult(`${e.result.path}: ${e.result.value}`)
                            })
                        }} type="button" className="btn btn-primary">Посчитать</button>
                    </div>
                </div>
            </div>
        </div>
    )
}


const Item = ({setItems, index,item, items})=>{
    return (
        <div className="input-group mb-3">
            <input type="text" value={item.from} onChange={(e)=>{
                item.from = e.target.value
                setItems([...items])
            }} className="form-control"  placeholder="From" />
            <span className="input-group-text">{"=>"}</span>
            <input onChange={(e)=>{
                item.to = e.target.value
                setItems([...items])
            }} type="text" className="form-control" value={item.to} placeholder="To" />
            <span className="input-group-text">=</span>
            <input onChange={(e)=>{
                item.value = e.target.value
                setItems([...items])
            }} type="text" className="form-control" value={item.value} placeholder="Value" />
            <button onClick={()=>{
                items.splice(index,1)
                setItems([...items])
            }} type="button" className="btn btn-danger">Удалить</button>
        </div>
    )
}

const Program2= ()=>{
    const [count,setCount] = useState(0)
    const [open,setOpen] = useState(false)
    const [save,setSave] = useState(false)
    const [items,setItems] = useState([])
    useEffect(()=>{
        get().then(e=>{
            setCount(1)
            setItems(e.items||[])
        })
    },[])
    useEffect(()=>{
        if(count<=1){
            setCount(2)
            return
        }
        setSave(true)
    },[items])
    return (
        <div className="container">
            <div className="block">
                <button type="button" className="btn btn-primary" onClick={()=>{
                    items.push({from:"",to:"", value:0})
                    setItems([...items])
                }} >Добавить</button>
                <button onClick={()=>{
                    update(items.map(e=>{
                        return {
                            from:e.from.toLocaleUpperCase(),
                            to:e.to.toLocaleUpperCase(),
                            value:parseInt(e.value)
                        }
                    })).then(e=>{
                        setSave(false)
                    })
                }} disabled={!save} type="button" className="btn btn-success">Сохранить</button>
                <button disabled={save} onClick={()=>setOpen(true)}  type="button" className="btn btn-info">Посчитать</button>
            </div>
            
            {items.map((e,i)=><Item items={items} item={e} setItems={setItems} index={i} key={i}/>)}
            {open&&<Modal setOpen={setOpen}/>}
        </div>
    )
}

export default Program2