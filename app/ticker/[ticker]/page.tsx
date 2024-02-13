async function getData(ticker: string){
  "use client"
  const data = await fetch(`http://localhost:8000/api/ticker/${ticker}`)
  return data.json()
}

export default async function Ticker({ params }: { params: { ticker: string } }) {

  const data = await getData(params.ticker);

  return (
    <main className="flex flex-wrap min-h-screen flex-col items-left justify-between p-24">
      <h1>{params.ticker}</h1>

      <h2>EMA</h2>
      <div >
        {JSON.stringify(data?.ema)}
      </div>

      <h2>MACD</h2>
      <div >
        {JSON.stringify(data?.macd)}
      </div>

    </main>)
}
