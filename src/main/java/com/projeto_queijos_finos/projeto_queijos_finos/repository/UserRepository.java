package com.projeto_queijos_finos.projeto_queijos_finos.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.projeto_queijos_finos.projeto_queijos_finos.entity.User;

public interface UserRepository extends JpaRepository<User, Long>{ 

}
