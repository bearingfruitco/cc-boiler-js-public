import { render, screen } from '@testing-library/react';
import { UserProfile } from '../UserProfile';

describe('UserProfile', () => {
  it('should render user name', () => {
    render(<UserProfile name="John Doe" />);
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });
});
