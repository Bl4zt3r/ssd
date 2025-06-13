import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

export default function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/contenedores').then(r => r.json()).then(setData);
  }, []);

  return (
    <MapContainer center={[0,0]} zoom={2} style={{height: '100vh'}}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {data.map(c => (
        <Marker key={c.id} position={[0,0]}>
          <Popup>Nivel: {c.nivel}%</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
