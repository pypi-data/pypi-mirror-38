'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('datasets', {
      id: {
        primaryKey: true,
        autoIncrement: true,
        type: Sequelize.INTEGER,
        allowNull: false
      },
      name: {
        allowNull: false,
        type: Sequelize.STRING,
        validate: {
          notEmpty: true
        },
      },
      description: {
        type: Sequelize.STRING
      },
      url: {
        type: Sequelize.STRING,
        validate: {
          isUrl: true
        }
      },
      uploader: {
        type: Sequelize.STRING,
        validate: {
          isEmail: true
        }
      },
      config: {
        type: Sequelize.JSON
      },
      createdAt: {
        allowNull: false,
        defaultValue: new Date(),
        type: Sequelize.DATE
      },
      updatedAt: {
        allowNull: false,
        defaultValue: new Date(),
        type: Sequelize.DATE
      }
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('datasets');
  }
};