export default function Disc({ player }: { player: number }) {
  const getDiscClass = () => {
    if (player === 1) return "disc human-disc";
    if (player === 2) return "disc ai-disc";
    return "disc empty-disc";
  };

  return <div className={getDiscClass()} />;
}