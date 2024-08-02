Sebastián Aguirre Rodriguez

Este diseño de base de datos ofrece una estructura flexible y extensible para la gestión integral de usuarios, roles, permisos y módulos. Permite una administración detallada de los permisos y el acceso dentro del sistema, garantizando que se cumplan los requisitos específicos de control de acceso. Las restricciones de unicidad implementadas en los modelos son fundamentales para mantener la integridad de los datos y evitar redundancias innecesarias.

Tras el análisis, identifique varias relaciones de muchos a muchos, como entre Roles y Usuarios, Usuarios y Permisos, y Roles y Permisos. Para gestionar estas interrelaciones de manera efectiva, decidí crear tablas intermedias (o tablas pivote) que facilitan la asignación de permisos a módulos y roles, y la relación entre usuarios y roles, asi como la asignación de permisos especiales. Esta decisión no solo previene redundancias y problemas de consistencia, sino que también asegura la escalabilidad del sistema a medida que se agregan más usuarios, roles y permisos.

Documentacion API: https://drive.google.com/file/d/15gqy1NJcEToGlv68BGUtlPpaUQ-nKwyy/view?usp=sharing