interface UserProfileProps {
  name: string;
}

export function UserProfile({ name }: UserProfileProps) {
  return (
    <div className="p-4 bg-white rounded-xl">
      <h2 className="text-size-2 font-semibold">{name}</h2>
    </div>
  );
}
