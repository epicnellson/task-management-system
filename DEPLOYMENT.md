# Task Manager Deployment Guide

This guide will help you deploy the Task Manager application to Railway.

## Prerequisites

1. A [Railway](https://railway.app) account
2. [Git](https://git-scm.com) installed on your computer
3. [Railway CLI](https://docs.railway.app/develop/cli) installed

## Deployment Steps

### 1. Prepare Your Application

1. Ensure all files are committed to your Git repository:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   ```

2. Verify your configuration files:
   - `railway.toml` - Railway configuration
   - `Procfile` - Process management
   - `requirements.txt` - Python dependencies

### 2. Deploy to Railway

1. Login to Railway:
   ```bash
   railway login
   ```

2. Initialize your project:
   ```bash
   railway init
   ```

3. Deploy your application:
   ```bash
   railway up
   ```

### 3. Configure Environment Variables

In the Railway dashboard:

1. Go to your project
2. Click on "Variables"
3. Add the following variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   DATABASE_URL=your-database-url
   VAPID_PUBLIC_KEY=your-vapid-public-key
   VAPID_PRIVATE_KEY=your-vapid-private-key
   ```

### 4. Set Up Custom Domain (Optional)

1. In Railway dashboard, go to your project
2. Click on "Settings"
3. Under "Domains", click "Generate Domain"
4. Follow the instructions to configure your domain

### 5. Verify Deployment

1. Visit your Railway-provided URL
2. Test the following features:
   - User registration and login
   - Task creation and management
   - Push notifications
   - Offline functionality
   - PWA installation

## PWA Installation Guide

### For Users

1. Open the application in Chrome/Edge
2. Click the install icon in the address bar
3. Click "Install" in the prompt
4. The app will be added to your home screen

### For Developers

To test PWA features locally:

1. Run the application:
   ```bash
   flask run
   ```

2. Open Chrome DevTools (F12)
3. Go to "Application" tab
4. Check:
   - Manifest
   - Service Workers
   - Cache Storage

## Troubleshooting

### Common Issues

1. **Service Worker Not Registering**
   - Ensure HTTPS is enabled
   - Check browser console for errors
   - Verify service worker file path

2. **Push Notifications Not Working**
   - Verify VAPID keys
   - Check notification permissions
   - Ensure service worker is registered

3. **Database Connection Issues**
   - Verify DATABASE_URL
   - Check database credentials
   - Ensure database is accessible

### Getting Help

If you encounter issues:

1. Check the [Railway documentation](https://docs.railway.app)
2. Review the [Flask documentation](https://flask.palletsprojects.com)
3. Open an issue in the project repository

## Maintenance

### Regular Tasks

1. Update dependencies:
   ```bash
   pip freeze > requirements.txt
   ```

2. Monitor application logs in Railway dashboard

3. Backup database regularly

### Security

1. Keep dependencies updated
2. Monitor security advisories
3. Regularly rotate secrets and keys

## Support

For support:
1. Open an issue in the project repository
2. Contact the development team
3. Check the documentation 