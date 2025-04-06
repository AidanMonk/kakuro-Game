import React from 'react'
import { useState, useEffect } from "react"
import { assets } from '../../assets/assets'
import './Main.css'
import Board from './Board'
import CustomButton from './ButtonTest';


const Main = () => {
    return (
        <main>
            <div className='header'>
                <h1>Welcome to Kakuro Game</h1>
            </div>
            <div className='gameplay'>

                <div className='instructions'>
                    <h2>How to play?</h2>
                    <p>
                        Kakuro is a fun and simple number puzzle game! Your goal is to fill the empty boxes in the grid with numbers from 1 to 9 so that the sums match the clues provided. Each clue represents the total you need to achieve in its corresponding row or column. The trick is that numbers in a row or column can’t repeat, so you need to think carefully about how to distribute them. Use logic and deduction to figure out the right numbers, and have fun solving the puzzle!
                    </p>
                </div>

                <div className="gamebox">
                    <Board/>
                </div>

                <div className="right-column">
                </div>

            </div>
        </main>
    )
}

export default Main;
