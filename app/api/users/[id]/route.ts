import { withErrorHandler, responses, ApiError } from '@/app/api/lib/handler';
import { createClient } from '@/lib/supabase/server';

export const GET = withErrorHandler(async (request, { params }) => {
  const supabase = createClient();
  
  // Get the user ID from params
  const { id } = params;
  
  // Fetch user from database
  const { data: user, error } = await supabase
    .from('users')
    .select('*')
    .eq('id', id)
    .single();
    
  if (error) {
    if (error.code === 'PGRST116') {
      throw new ApiError(404, 'User not found');
    }
    throw error;
  }
  
  return responses.success(user);
});

export const PATCH = withErrorHandler(async (request, { params }) => {
  const supabase = createClient();
  const { id } = params;
  
  // Get the current user
  const { data: { user: currentUser } } = await supabase.auth.getUser();
  
  if (!currentUser) {
    return responses.unauthorized();
  }
  
  // Check if user is updating their own profile
  if (currentUser.id !== id) {
    return responses.forbidden('You can only update your own profile');
  }
  
  // Parse and validate the request body
  const body = await request.json();
  
  // Update user
  const { data: user, error } = await supabase
    .from('users')
    .update(body)
    .eq('id', id)
    .select()
    .single();
    
  if (error) {
    throw error;
  }
  
  return responses.success(user);
});

export const DELETE = withErrorHandler(async (request, { params }) => {
  const supabase = createClient();
  const { id } = params;
  
  // Get the current user
  const { data: { user: currentUser } } = await supabase.auth.getUser();
  
  if (!currentUser) {
    return responses.unauthorized();
  }
  
  // Check if user is deleting their own account
  if (currentUser.id !== id) {
    return responses.forbidden('You can only delete your own account');
  }
  
  // Delete user
  const { error } = await supabase
    .from('users')
    .delete()
    .eq('id', id);
    
  if (error) {
    throw error;
  }
  
  return responses.noContent();
});
