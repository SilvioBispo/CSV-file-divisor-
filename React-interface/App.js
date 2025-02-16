import './App.css'
import api from './Api'
import {useState} from 'react'

function App(){

   const [nome,setnome] = useState([])
   const [file,setfile] = useState([])
    async function get_tables() {
       const tables_api =  await api.get('/')
        setnome(tables_api.data)
    }

    async function post_file() {
        const  files = new FormData();
        files.append('file', file)
        await api.post('/',files,{
            headers:{
                'Content-Type': 'multipart/form-data'
            }
        } )
    }

    async function create_tables() {
        await api.get('/tables')
    }

    async function delete_table(nome) {
        await api.delete('/',{
            data: {file: nome}
        })
        get_tables()  
    }

    async function delete_all() {
        await api.delete('/delete_all')
        get_tables()
    }

    async function put_table(params) {
        const  files = new FormData();
        files.append('file', file)
        await api.put('/',files,{
            headers:{
                'Content-Type': 'multipart/form-data'
            }
        } )
    }
    return (<>
        <div>
            <input type="file"  className='input' onChange={(e) => {setfile(e.target.files[0])}} />
        </div>
        <div className='div'>
            <button className='button-put' onClick={post_file}>Input file</button>
            <button className='button-put' onClick={create_tables}>Create Tables</button>
            <button id="delete_all_button" className='button-delete-all' onClick={delete_all}>Delete all</button>
            <button className='button-put' onClick={get_tables}>show tables</button>
        </div>
        <div>
            <table className='styled-table'>
                <thead>
                <tr>
                    <th>File</th>
                    <th>Actions</th>
                    <th></th>
                </tr>
                </thead>
                <tbody>
                {nome.map((nome) => (<tr>
                    <td>{nome}</td>
                    <td><button className='button-put' onClick={put_table}>update</button></td>
                    <td><button className='button-delete' onClick={(e) => delete_table(nome.toString())}>delete</button></td>
                </tr>))}
                </tbody>
            </table>
        </div>
    </>
) 
}

export default App