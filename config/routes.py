class Routes:
	REGISTRATION = '/registration'
	LOGIN = '/login'
	USERNAME_IS_EXISTS = '/username_is_exists'
	GET_MY_USER_DATA = '/get_my_user_data'
	GET_USER = '/user'
	GET_USERS = '/users'

	AUTHORIZED_ROUTES = (
		GET_MY_USER_DATA,
		GET_USER,
		GET_USERS,
	)