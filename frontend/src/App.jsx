import { Fragment, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import {useEffect } from 'react'

// const host="http://127.0.0.1:8000/"
const host=""

function App() {
  return <div className='h-screen w-screen m-0 p-4'>
    {/* <TestComponent/> */}
    <FormComponent/>
  </div>
    
}

function FormComponent(){
    const [message,setMessage]=useState("");
    const [loading,setLoading]=useState(false);
    const [result,setResult]=useState("");

    function handleChange(e){
      e.preventDefault();
      setMessage(e.target.value)
    }

    function clickHandler(e){
      e.preventDefault()
      setLoading(true);
      fetch(`${host}/predict`,{
        method:"POST",
        body:JSON.stringify({
          message:message
        })
      })
      .then(res=>res.json())
      .then(res=>{
        setLoading(false);
        setResult(res.result);
      })
      .catch(err=>{
        setLoading(false);
        window.alert(err.message);
      })
    }

    return <Fragment>
      <div className='mt-5 flex flex-col gap-6 items-center'>
          <form className='flex flex-col gap-4 w-1/2 h-auto border-2 border-black rounded-md p-4 bg-slate-200'>
              <label htmlFor="msg" className='font-semibold text-xl' >Spam Detection</label>
              <textarea type="text" className='border-1 border-black p-2' id='msg' value={message} placeholder='Enter the message' rows={15} onChange={handleChange} />

              {result=="spam" && <button className='p-2 rounded-md bg-red-700  text-white' disabled={true}>Spam</button>}
              {result=="ham" && <button className='p-2 rounded-md bg-green-700  text-white' disabled={true}>Ham</button>}

              {!loading?<button className='p-2 rounded-md bg-blue-800 text-white' onClick={clickHandler}>Predict</button>
              : <button className='p-2 rounded-md bg-blue-700 animate-pulse text-white'>Predicting..</button>
              }
              <button className='p-2 rounded-md bg-blue-400 text-white' onClick={(e)=>{e.preventDefault();setMessage("");setResult("");}}>Clear</button>

              
          </form>
      </div>
    </Fragment>
}

function TestComponent(){
  // useEffect(()=>{
  //   fetch(`${host}/test`)
  //   .then((res)=>res.json())
  //   .then(res=>console.log(res))
  //   .catch(err=>console.log(err.message))
  // },[]);
  useEffect(()=>{
    fetch(`${host}/predict`,{
      method:"POST",
      body:JSON.stringify({
        message:"I am tonmoy"
      })
    })
    .then((res)=>res.json())
    .then(res=>console.log(res))
    .catch(err=>console.log(err.message))
  },[]);
  return (
    <h1 className='text-white font-bold text-2xl p-4' >
      Hello world!
    </h1>
  )
}



export default App
