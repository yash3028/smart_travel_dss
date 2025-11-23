import { Entity, PrimaryGeneratedColumn, Column } from "typeorm";

@Entity()
export class users {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column()
  name!: string;

  @Column({ unique: true })
  username!: string;

  @Column()
  password!: string;

  @Column({ default: null })
  token!: string;
}
