"use client"

import useSWR from 'swr'

export default function Ticker({ params }: { params: { ticker: string } }) {

  const { data, error, isLoading } = useSWR(`/api/ticker/${params.ticker}`, (url) => fetch(url).then((res) => res.json()));
  console.log("Data: ", data);
  console.log("Err: ", error);
  console.log("Loading: ", isLoading);

  return (
    <main className="flex flex-wrap min-h-screen flex-col items-left justify-between p-24">
      <h1>{params.ticker}</h1>
      {error && <div>failed to load</div>}
      {isLoading && <div>loading...</div>}

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
